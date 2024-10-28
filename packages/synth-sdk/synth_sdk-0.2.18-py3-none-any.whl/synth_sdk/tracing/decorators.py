from typing import Callable, Optional, Set, Literal, Any
from functools import wraps
import threading
import time
from synth_sdk.tracing.abstractions import Event, AgentComputeStep
from synth_sdk.tracing.events.store import event_store
import logging
import inspect

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
    """
    Set the current event, ending any existing events of the same type.
    """
    logger.debug(f"Setting current event of type {event.event_type}")
    
    if not hasattr(_local, "active_events"):
        _local.active_events = {}
        logger.debug("Initialized active_events in thread local storage")
    
    # If there's an existing event of the same type, end it
    if event.event_type in _local.active_events:
        logger.debug(f"Found existing event of type {event.event_type}")
        existing_event = _local.active_events[event.event_type]
        existing_event.closed = time.time()
        # Store the event if we have a system_id
        if hasattr(_local, "system_id"):
            logger.debug(f"Storing existing event for system {_local.system_id}")
            try:
                event_store.add_event(_local.system_id, existing_event)
                logger.debug("Successfully stored existing event")
            except Exception as e:
                logger.error(f"Failed to store existing event: {str(e)}")
                raise
    else:
        logger.debug(f"No existing event of type {event.event_type}")
    
    # Set the new event
    _local.active_events[event.event_type] = event
    logger.debug("New event set as current")


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
    log_vars_input: Optional[Set[str]] = None,
    log_vars_output: Optional[Set[str]] = None,
    log_result: bool = False,
    manage_event: Literal["create", "end", None] = None,
    increment_partition: bool = False,
    verbose: bool = False,
) -> Callable:
    """
    Decorator for tracing agent compute steps.

    Args:
        event_type: The type of event this compute step belongs to
        log_vars_input: Set of variable names to log from the function's arguments or local variables
        log_vars_output: Set of variable names to log from the function's return value or local variables
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

                # Capture input variables from arguments and prepare for local scope capture
                compute_input = {}
                if log_vars_input:
                    bound_args = inspect.signature(func).bind(self, *args, **kwargs)
                    bound_args.apply_defaults()
                    args_dict = bound_args.arguments
                    for var in log_vars_input:
                        if var in args_dict:
                            compute_input[var] = args_dict[var]
                        else:
                            # Variable not found in arguments; will attempt to capture from local scope after execution
                            if verbose:
                                logger.debug(f"Variable '{var}' not found in arguments. Will attempt to capture from local scope.")
                
                # Execute function
                start_time = time.time()
                if verbose:
                    logger.debug("Executing wrapped function")
                
                # Capture the frame before function execution
                frame_before = inspect.currentframe()
                try:
                    result = func(self, *args, **kwargs)
                finally:
                    frame_before = None  # Prevent reference cycles

                end_time = time.time()
                if verbose:
                    logger.debug(f"Function completed in {end_time - start_time:.2f}s")

                # Capture the frame after function execution to access local variables
                frame_after = inspect.currentframe()
                try:
                    # Attempt to retrieve the frame where the function was executed
                    outer_frames = inspect.getouterframes(frame_after)
                    func_frame = outer_frames[1].frame if len(outer_frames) > 1 else None

                    if func_frame:
                        local_vars = func_frame.f_locals
                        # Populate compute_input from local variables if not found in arguments
                        if log_vars_input:
                            for var in log_vars_input:
                                if var not in compute_input and var in local_vars:
                                    compute_input[var] = local_vars[var]
                                elif var not in compute_input and var not in local_vars:
                                    if verbose:
                                        logger.error(f"Variable '{var}' specified in log_vars_input not found in function arguments or local scope")
                                    raise ValueError(f"Variable '{var}' specified in log_vars_input not found in function arguments or local scope")
                    else:
                        local_vars = {}
                        if verbose:
                            logger.error("Unable to retrieve function's frame for capturing local variables.")

                finally:
                    frame_after = None  # Prevent reference cycles

                # Capture output variables based on return type and local variables
                compute_output = {}

                if log_vars_output:
                    if isinstance(result, dict):
                        for var in log_vars_output:
                            if var in result:
                                compute_output[var] = result[var]
                            elif var in local_vars:
                                compute_output[var] = local_vars[var]
                            elif hasattr(self, var):  # Check self for the variable
                                compute_output[var] = getattr(self, var)
                            else:
                                if verbose:
                                    logger.error(f"Variable '{var}' specified in log_vars_output not found in result, local scope, or 'self'")
                                raise ValueError(f"Variable '{var}' specified in log_vars_output not found in result, local scope, or 'self'")
                    elif isinstance(result, (tuple, list)):
                        if len(log_vars_output) > len(result):
                            # Attempt to get remaining variables from local scope or 'self'
                            for i, var in enumerate(log_vars_output):
                                if i < len(result):
                                    compute_output[var] = result[i]
                                elif var in local_vars:
                                    compute_output[var] = local_vars[var]
                                elif hasattr(self, var):  # Check self for the variable
                                    compute_output[var] = getattr(self, var)
                                else:
                                    if verbose:
                                        logger.error(f"Variable '{var}' specified in log_vars_output not found in result, local scope, or 'self'")
                                    raise ValueError(f"Variable '{var}' specified in log_vars_output not found in result, local scope, or 'self'")
                        else:
                            for var, value in zip(log_vars_output, result):
                                compute_output[var] = value
                            # If there are more variables to capture than the result provides
                            extra_vars = set(log_vars_output) - set([var for var, _ in zip(log_vars_output, result)])
                            for var in extra_vars:
                                if var in local_vars:
                                    compute_output[var] = local_vars[var]
                                elif hasattr(self, var):  # Check self for the variable
                                    compute_output[var] = getattr(self, var)
                                else:
                                    if verbose:
                                        logger.error(f"Variable '{var}' specified in log_vars_output not found in result, local scope, or 'self'")
                                    raise ValueError(f"Variable '{var}' specified in log_vars_output not found in result, local scope, or 'self'")
                    else:
                        # Single return value
                        for var in log_vars_output:
                            if var == 'result':
                                compute_output[var] = result
                            elif var in local_vars:
                                compute_output[var] = local_vars[var]
                            elif hasattr(self, var):  # Check self for the variable
                                compute_output[var] = getattr(self, var)
                            else:
                                # If the variable isn't found in locals or 'self', assume it's meant to capture the return value
                                compute_output[var] = result

                if log_result:
                    compute_output['result'] = result

                # Populate compute_input from log_vars_input
                if log_vars_input:
                    # compute_input already populated from arguments and local scope
                    pass

                # Create compute step and append to current event
                compute_step = AgentComputeStep(
                    event_order=len(current_event.agent_compute_steps),
                    compute_began=start_time,
                    compute_ended=end_time,
                    compute_input=compute_input,
                    compute_output=compute_output,
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
