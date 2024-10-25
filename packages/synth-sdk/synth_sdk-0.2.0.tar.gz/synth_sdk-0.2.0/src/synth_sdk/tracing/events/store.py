import json
import threading
from typing import Dict, List, Optional
from src.synth_sdk.tracing.abstractions import (
    SystemTrace, EventPartitionElement, Event
)
from src.synth_sdk.tracing import tracer

class EventStore:
    def __init__(self):
        self._events: Dict[str, List[Event]] = {}
        self._system_traces: Dict[str, SystemTrace] = {}
        self._lock = threading.Lock()

    def get_or_create_system_trace(self, system_id: str) -> SystemTrace:
        """Get or create a SystemTrace for the given system_id."""
        with self._lock:
            if system_id not in self._system_traces:
                self._system_traces[system_id] = SystemTrace(
                    system_id=system_id,
                    partition=[EventPartitionElement(partition_index=0, events=[])],
                    current_partition_index=0
                )
            return self._system_traces[system_id]

    def increment_partition(self, system_id: str) -> int:
        """Increment the partition index for a system and create new partition element."""
        with self._lock:
            system_trace = self.get_or_create_system_trace(system_id)
            system_trace.current_partition_index += 1
            system_trace.partition.append(
                EventPartitionElement(
                    partition_index=system_trace.current_partition_index,
                    events=[]
                )
            )
            return system_trace.current_partition_index

    def add_event(self, system_id: str, event: Event):
        """Add an event to the appropriate partition of the system trace."""
        with self._lock:
            system_trace = self.get_or_create_system_trace(system_id)
            
            # Find the current partition element
            current_partition = next(
                (p for p in system_trace.partition 
                 if p.partition_index == event.partition_index),
                None
            )
            
            if current_partition is None:
                raise ValueError(
                    f"No partition found for index {event.partition_index} "
                    f"in system {system_id}"
                )

            current_partition.events.append(event)

            # Create a span for the event
            with tracer.start_as_current_span(event.event_type) as span:
                span.set_attribute("system.id", system_id)
                span.set_attribute("event.opened", event.opened)
                span.set_attribute("event.closed", event.closed)
                span.set_attribute("event.partition_index", event.partition_index)

                for step in event.agent_compute_steps:
                    span.add_event(
                        "agent_compute",
                        {
                            "order": step.event_order,
                            "began": step.compute_began,
                            "ended": step.compute_ended,
                            "input": step.compute_input,
                            "output": step.compute_output,
                        },
                    )

    def get_system_traces(self) -> List[SystemTrace]:
        """Get all system traces."""
        with self._lock:
            return list(self._system_traces.values())

    def get_system_traces_json(self) -> str:
        """Get all system traces as JSON."""
        with self._lock:
            return json.dumps([
                {
                    "system_id": trace.system_id,
                    "current_partition_index": trace.current_partition_index,
                    "partition": [
                        {
                            "partition_index": p.partition_index,
                            "events": [self._event_to_dict(event) for event in p.events]
                        }
                        for p in trace.partition
                    ]
                }
                for trace in self._system_traces.values()
            ], default=str)

    def _event_to_dict(self, event: Event) -> dict:
        """Convert an Event object to a dictionary."""
        return {
            "event_type": event.event_type,
            "opened": event.opened,
            "closed": event.closed,
            "partition_index": event.partition_index,
            "agent_compute_steps": [
                {
                    "event_order": step.event_order,
                    "compute_began": step.compute_began,
                    "compute_ended": step.compute_ended,
                    "compute_input": step.compute_input,
                    "compute_output": step.compute_output,
                }
                for step in event.agent_compute_steps
            ],
            "environment_compute_steps": [
                {
                    "event_order": step.event_order,
                    "compute_began": step.compute_began,
                    "compute_ended": step.compute_ended,
                    "compute_input": step.compute_input,
                    "compute_output": step.compute_output,
                }
                for step in event.environment_compute_steps
            ]
        }

# Global event store instance
event_store = EventStore()
