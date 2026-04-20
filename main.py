# main.py
# Run with: uvicorn main:app --reload

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import re

app = FastAPI(
    title="Agent Discovery Platform",
    version="1.0.0"
)

# -----------------------------
# In-memory storage
# -----------------------------

agents_db = {}
usage_db = {}
seen_requests = set()

# -----------------------------
# Models
# -----------------------------

class Agent(BaseModel):
    name: str
    description: str
    endpoint: str


class UsageLog(BaseModel):
    caller: str
    target: str
    units: int
    request_id: str


# -----------------------------
# Keyword Extraction
# -----------------------------

STOPWORDS = {
    "a", "an", "the", "is", "are",
    "to", "of", "in", "for", "and",
    "or", "with", "on", "at"
}


def extract_tags(description: str) -> List[str]:

    words = re.findall(
        r"\b[a-zA-Z]{3,}\b",
        description.lower()
    )

    tags = []

    for word in words:
        if word not in STOPWORDS:
            tags.append(word)

    return sorted(set(tags))


# -----------------------------
# POST /agents
# -----------------------------

@app.post("/agents", status_code=201)
def add_agent(agent: Agent):

    if agent.name in agents_db:
        return {
            "message": "Agent already registered",
            "agent": agents_db[agent.name]
        }

    record = agent.dict()

    record["tags"] = extract_tags(
        agent.description
    )

    agents_db[agent.name] = record

    return {
        "message": "Agent registered",
        "agent": record
    }


# -----------------------------
# GET /agents
# -----------------------------

@app.get("/agents")
def list_agents():

    return list(
        agents_db.values()
    )


# -----------------------------
# GET /search
# -----------------------------

@app.get("/search")
def search_agents(
    q: str = Query(..., min_length=1)
):

    q_lower = q.lower()

    results = []

    for agent in agents_db.values():

        if (
            q_lower in agent["name"].lower()
            or
            q_lower in agent["description"].lower()
        ):
            results.append(agent)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }


# -----------------------------
# POST /usage
# -----------------------------

@app.post("/usage")
def log_usage(
    usage: UsageLog
):

    # Unknown agent check

    if usage.target not in agents_db:

        raise HTTPException(
            status_code=404,
            detail="Target agent not registered"
        )

    # Duplicate request check

    if usage.request_id in seen_requests:

        return {
            "message":
            "Duplicate request_id ignored"
        }

    seen_requests.add(
        usage.request_id
    )

    usage_db[usage.target] = (
        usage_db.get(
            usage.target,
            0
        )
        + usage.units
    )

    return {
        "message": "Usage logged"
    }


# -----------------------------
# GET /usage-summary
# -----------------------------

@app.get("/usage-summary")
def usage_summary():

    sorted_summary = dict(
        sorted(
            usage_db.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    return {
        "summary": sorted_summary
    }


# -----------------------------
# Health check
# -----------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "agents_registered":
            len(agents_db),
        "unique_requests_logged":
            len(seen_requests)
    }