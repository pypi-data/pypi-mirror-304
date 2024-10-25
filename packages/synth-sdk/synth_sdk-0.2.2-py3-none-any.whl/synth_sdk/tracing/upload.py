from typing import List, Union, Optional
from pydantic import BaseModel
import requests
import logging
import os
from src.synth_sdk.tracing.events.store import event_store

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
    system_id: str
    reward: Union[float, int, bool]
    annotation: Optional[str] = None

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "system_id": self.system_id,
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

def send_system_traces(dataset: Dataset, base_url: str, api_key: str) -> requests.Response:
    """Send all system traces and dataset metadata to the server."""
    # Get the token using the API key
    token_url = f"{base_url}/token"
    token_response = requests.get(
        token_url, 
        headers={"customer_specific_api_key": api_key}
    )
    token_response.raise_for_status()
    access_token = token_response.json()["access_token"]

    # Get traces as JSON
    traces_json = event_store.get_system_traces_json()

    # Send the traces with the token
    api_url = f"{base_url}/upload/"
    payload = {
        "system_traces": traces_json,
        "dataset": dataset.to_dict()
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Upload ID: {response.json().get('upload_id')}")
        return response
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        raise

async def upload(dataset: Dataset, verbose: bool = False):
    """Upload all system traces and dataset to the server."""
    api_key = os.getenv("SYNTH_API_KEY")
    if not api_key:
        raise ValueError("SYNTH_API_KEY environment variable not set")

    response = send_system_traces(
        dataset=dataset,
        base_url="https://agent-learning.onrender.com", 
        api_key=api_key
    )
    
    if verbose:
        print("Response status code:", response.status_code)
        if response.status_code == 202:
            traces = event_store.get_system_traces()
            print(f"Upload successful - sent {len(traces)} system traces.")
            print(f"Dataset included {len(dataset.questions)} questions and {len(dataset.reward_signals)} reward signals.")
            
    return response

