from typing import Callable, Optional, Set, Literal
from functools import wraps
import threading
import time
from synth_sdk.tracing.abstractions import Event, AgentComputeStep
from synth_sdk.tracing.events.store import event_store
import logging

logger = logging.getLogger(__name__)

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


def set_system_id(system_id: str):
    """Set the system_id in thread local storage."""
    _local.system_id = system_id


def trace_system(
    event_type: str,
    log_vars: Optional[Set[str]] = None,
    log_result: bool = False,
    manage_event: Literal["create", "end", None] = None,
    increment_partition: bool = False,
    verbose: bool = False,
) -> Callable:
    """
    Decorator for tracing agent compute steps.

    Args:
        event_type: The type of event this compute step belongs to
        log_vars: Set of variable names to log from the local scope
        log_result: Whether to log the function's return value
        manage_event: Controls event lifecycle
        increment_partition: Whether to increment the partition counter
        verbose: Whether to enable debug logging
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if verbose:
                logger.debug(f"Enter trace_system decorator for {func.__name__}")
            
            try:
                # Set system_id from instance attribute if it exists
                if hasattr(self, 'system_id'):
                    if verbose:
                        logger.debug(f"Found system_id: {self.system_id}")
                    _local.system_id = self.system_id
                
                if not hasattr(_local, "system_id"):
                    if verbose:
                        logger.debug("No system_id found")
                    raise ValueError("system_id not set")

                # Increment partition if requested
                if increment_partition:
                    if verbose:
                        logger.debug("Incrementing partition")
                    current_partition = event_store.increment_partition(_local.system_id)
                else:
                    current_partition = event_store.get_or_create_system_trace(
                        _local.system_id
                    ).current_partition_index

                # Create event if requested
                if manage_event == "create":
                    if verbose:
                        logger.debug("Creating new event")
                    new_event = Event(
                        event_type=event_type,
                        opened=time.time(),
                        closed=None,
                        partition_index=current_partition,
                        agent_compute_steps=[],
                        environment_compute_steps=[],
                    )
                    set_current_event(new_event)

                # Get current event
                try:
                    current_event = get_current_event(event_type)
                    if verbose:
                        logger.debug("Retrieved current event")
                except ValueError as e:
                    if verbose:
                        logger.error(f"Event error: {e}")
                    raise

                # Execute function
                start_time = time.time()
                if verbose:
                    logger.debug("Executing wrapped function")
                result = func(self, *args, **kwargs)
                end_time = time.time()
                if verbose:
                    logger.debug(f"Function completed in {end_time - start_time:.2f}s")

                # Create compute step
                compute_step = AgentComputeStep(
                    event_order=len(current_event.agent_compute_steps),
                    compute_began=start_time,
                    compute_ended=end_time,
                    compute_input=None,
                    compute_output=None,
                )
                current_event.agent_compute_steps.append(compute_step)

                # End event if requested
                if manage_event == "end":
                    if verbose:
                        logger.debug("Ending event")
                    current_event.closed = time.time()
                    event_store.add_event(_local.system_id, current_event)
                    clear_current_event(event_type)

                return result

            except Exception as e:
                if verbose:
                    logger.error(f"Error in decorator: {str(e)}", exc_info=True)
                raise
            finally:
                if verbose:
                    logger.debug(f"Exit trace_system decorator for {func.__name__}")

        return wrapper

    return decorator
