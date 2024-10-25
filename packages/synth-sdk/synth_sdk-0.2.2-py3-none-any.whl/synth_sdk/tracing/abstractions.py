from dataclasses import dataclass
from typing import Any, List, Dict, Optional

@dataclass
class ComputeStep:
    event_order: int
    compute_ended: Any  # time step
    compute_began: Any  # time step
    compute_input: Any  # json?
    compute_output: Any  # json?

class AgentComputeStep(ComputeStep):
    pass

class EnvironmentComputeStep(ComputeStep):
    pass

@dataclass
class Event:
    event_type: str
    opened: Any  # time stamp
    closed: Any  # time stamp
    partition_index: int  # New field
    agent_compute_steps: List[AgentComputeStep]
    environment_compute_steps: List[EnvironmentComputeStep]

@dataclass
class EventPartitionElement:
    partition_index: int
    events: List[Event]

@dataclass
class SystemTrace:
    system_id: str
    partition: List[EventPartitionElement]
    current_partition_index: int = 0  # Track current partition
