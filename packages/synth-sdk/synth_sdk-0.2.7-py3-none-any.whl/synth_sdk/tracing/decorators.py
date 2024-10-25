from typing import Callable, Optional, Set, Literal
from functools import wraps
import threading
import time
from synth_sdk.tracing.abstractions import Event, AgentComputeStep
from synth_sdk.tracing.events.store import event_store
import sys

# Thread-local storage for active events
_local = threading.local()


def get_current_event(event_type: str) -> "Event":
    """
    Get the current active event of the specified type.
    Raises ValueError if no such event exists.
    """
    events = getattr(_local, "active_events", {})
    if event_type not in events:
        raise ValueError(f"No active event of type '{event_type}' found")
    return events[event_type]


def set_current_event(event: "Event"):
    if not hasattr(_local, "active_events"):
        _local.active_events = {}
    _local.active_events[event.event_type] = event


def clear_current_event(event_type: str):
    if hasattr(_local, "active_events"):
        _local.active_events.pop(event_type, None)


def end_event() -> Optional[Event]:
    """End the current event and store it."""
    current_event = get_current_event()
    if current_event:
        current_event.closed = time.time()
        # Store the event
        if hasattr(_local, "system_id"):
            event_store.add_event(_local.system_id, current_event)
        set_current_event(None)
    return current_event


def trace_system(
    event_type: str,
    log_vars: Optional[Set[str]] = None,
    log_result: bool = False,
    manage_event: Literal["create", "end", None] = None,
    increment_partition: bool = False,
) -> Callable:
    """
    Decorator for tracing agent compute steps.

    Args:
        event_type: The type of event this compute step belongs to
        log_vars: Set of variable names to log from the local scope
        log_result: Whether to log the function's return value
        manage_event: Controls event lifecycle
        increment_partition: Whether to increment the partition counter
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(_local, "system_id"):
                raise ValueError("system_id not set in thread local storage")

            # Increment partition if requested
            if increment_partition:
                current_partition = event_store.increment_partition(_local.system_id)
            else:
                current_partition = event_store.get_or_create_system_trace(
                    _local.system_id
                ).current_partition_index

            # Create event if requested
            if manage_event == "create":
                new_event = Event(
                    event_type=event_type,
                    opened=time.time(),
                    closed=None,
                    partition_index=current_partition,
                    agent_compute_steps=[],
                    environment_compute_steps=[],
                )
                set_current_event(new_event)

            try:
                # Get the current event of this type
                current_event = get_current_event(event_type)
            except ValueError as e:
                raise ValueError(
                    f"Cannot add compute step: {str(e)}. "
                    f"Did you forget to wrap this in 'with event_scope('{event_type}')'?"
                ) from e

            # Start timing
            start_time = time.time()

            # Create a dict to store logged variables
            logged_data = {}

            try:
                result = func(self, *args, **kwargs)

                # Log specified local variables
                if log_vars:
                    # Get function's local variables
                    frame = sys._getframe()
                    local_vars = frame.f_locals

                    for var_name in log_vars:
                        if var_name in local_vars:
                            logged_data[var_name] = local_vars[var_name]

                # Log result if requested
                if log_result:
                    logged_data["result"] = result

                # Create compute step
                compute_step = AgentComputeStep(
                    event_order=len(current_event.agent_compute_steps),
                    compute_began=start_time,
                    compute_ended=time.time(),
                    compute_input=logged_data if logged_data else None,
                    compute_output=None,  # We're using compute_input for all logging
                )

                # Add to current event
                current_event.agent_compute_steps.append(compute_step)

                # End event if requested
                if manage_event == "end":
                    current_event.closed = time.time()
                    if hasattr(_local, "system_id"):
                        event_store.add_event(_local.system_id, current_event)
                    clear_current_event(event_type)

                return result

            except Exception as e:
                # Log error in compute step
                compute_step = AgentComputeStep(
                    event_order=len(current_event.agent_compute_steps),
                    compute_began=start_time,
                    compute_ended=time.time(),
                    compute_input=logged_data if logged_data else None,
                    compute_output={"error": str(e)},
                )
                current_event.agent_compute_steps.append(compute_step)

                # End event even on error if requested
                if manage_event == "end":
                    current_event.closed = time.time()
                    if hasattr(_local, "system_id"):
                        event_store.add_event(_local.system_id, current_event)
                    clear_current_event(event_type)
                raise

        return wrapper

    return decorator
