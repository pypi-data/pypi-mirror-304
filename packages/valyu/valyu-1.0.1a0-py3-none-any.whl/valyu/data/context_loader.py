import json
import requests
from pydantic import BaseModel
from typing import List, Dict, Any
import os

CONTEXT_API_ENDPOINT = 'http://ec2-18-135-104-194.eu-west-2.compute.amazonaws.com:6000/query'

class ContextMatch(BaseModel):
    id: str
    index: str
    score: float
    text: str

class ContextResponse(BaseModel):
    top_k_matches: List[ContextMatch]

class Context:
    def __init__(self, data_sources, credit_budget):
        self.data_sources = data_sources
        self.credit_budget = credit_budget
        self.top_k = 2

    def fetch_context(self, query: str) -> ContextResponse:
        try:
            print(f"Fetching context for query: {query}\n")
            response = requests.post(CONTEXT_API_ENDPOINT, json={
                "query": query,
                "budget": 1000,
                "db_store": [source for source in self.data_sources],
                "top_k": self.top_k
            })
            response.raise_for_status()
            data = response.json()
            # print(f"Response data: {data}")

            if "response" in data and "top_k_matches" in data["response"]:
                matches = [ContextMatch(
                    id=match['_id'],
                    index=match['_index'],
                    score=match['_score'],
                    text=match['_source']['text']
                ) for match in data["response"]["top_k_matches"][:self.top_k]]
                return ContextResponse(top_k_matches=matches)
            else:
                print("Unexpected response format")
                return None
        except requests.RequestException as e:
            print(f"Error fetching context: {e}")
            return None
