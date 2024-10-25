from dataclasses import dataclass
from typing import Any, List, Dict, Optional, Union
from pydantic import BaseModel

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


class TrainingQuestion(BaseModel):
    intent: str
    criteria: str
    question_id: Optional[str] = None

    def to_dict(self):
        return {
            "intent": self.intent,
            "criteria": self.criteria,
        }


class RewardSignal(BaseModel):
    question_id: Optional[str] = None
    agent_id: str
    reward: Union[float, int, bool]
    annotation: Optional[str] = None

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "agent_id": self.agent_id,
            "reward": self.reward,
            "annotation": self.annotation,
        }


class Dataset(BaseModel):
    questions: List[TrainingQuestion]
    reward_signals: List[RewardSignal]

    def to_dict(self):
        return {
            "questions": [question.to_dict() for question in self.questions],
            "reward_signals": [signal.to_dict() for signal in self.reward_signals],
        }
