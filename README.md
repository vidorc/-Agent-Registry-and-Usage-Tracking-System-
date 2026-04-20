# Agent Registry and Usage Tracking System

## Overview

This project implements a simplified **Agent Discovery and Usage Platform** using Python and FastAPI.

The system allows agents (services) to be:

* Registered
* Discovered through search
* Used by other agents
* Tracked through usage logs
* Aggregated into usage summaries

The design focuses on simplicity, correctness, and handling real-world edge cases such as duplicate requests and invalid input.

The application runs locally using in-memory storage and follows REST API principles.

---

## Features

### 1. Agent Registration

Users can register new agents with:

* Name
* Description
* Endpoint

The system automatically generates keywords (tags) from the description.

Duplicate registrations are handled safely (idempotent behavior).

---

### 2. Agent Search

Agents can be searched using:

* Name
* Description

Search is:

* Case-insensitive
* Simple substring matching

Example:

GET /search?q=pdf

---

### 3. Usage Logging

Agents can log interactions with other agents.

Each usage request includes:

* Caller
* Target
* Units
* Request ID

Important behavior:

* Duplicate request_id values are ignored
* Unknown agents return an error

This ensures reliable and consistent usage tracking.

---

### 4. Usage Summary

The system aggregates total usage per agent.

Example output:

DocParser → 120
Summarizer → 80

Results are sorted in descending order.

---

### 5. Keyword Extraction

Simple keyword extraction is implemented without using an LLM.

The system:

* Extracts words from the description
* Removes common stopwords
* Stores unique tags

This demonstrates basic AI-style logic using deterministic rules.

---

## API Endpoints

### Register Agent

POST /agents

Example request:

{
"name": "DocParser",
"description": "Extracts structured data from PDFs",
"endpoint": "https://api.example.com/parse"
}

---

### List Agents

GET /agents

Returns all registered agents.

---

### Search Agents

GET /search?q=keyword

Performs case-insensitive search on:

* name
* description

---

### Log Usage

POST /usage

Example request:

{
"caller": "AgentA",
"target": "DocParser",
"units": 10,
"request_id": "abc123"
}

Behavior:

* Duplicate request_id is ignored
* Unknown target returns error

---

### Usage Summary

GET /usage-summary

Returns total usage per agent.

---

### Health Check

GET /health

Returns:

* System status
* Number of agents
* Number of logged requests

---

## Project Structure

project-folder/

main.py
requirements.txt
README.md

---

## Requirements

Python 3.9 or later

Install dependencies:

pip install fastapi uvicorn pydantic

Or:

pip install -r requirements.txt

---

## Running the Application

Start the server:

uvicorn main:app --reload

Open the API documentation:

http://127.0.0.1:8000/docs

---

## Edge Cases Handled

The system correctly handles:

* Duplicate request_id (idempotency)
* Unknown agent usage
* Missing fields validation
* Case-insensitive search
* Empty usage data

These behaviors improve reliability in real-world systems.

---

## Design Decisions

### Why In-Memory Storage?

The assignment required:

* Simple implementation
* Local execution
* No over-engineering

In-memory storage satisfies these requirements while keeping the system easy to understand.

---

### Idempotency

Duplicate requests are prevented using:

request_id

If the same request is sent twice:

The second request is ignored.

This prevents double counting and ensures data consistency.

---

### Keyword Extraction

Instead of using AI models, a rule-based approach was used:

* Regex word extraction
* Stopword filtering
* Unique tag generation

This keeps the system simple and predictable.

---

## Scaling Considerations

If the system grows to support many agents:

Possible improvements:

* Replace in-memory storage with PostgreSQL
* Add indexing for search
* Partition usage logs by date
* Use message queues for high write volume

These changes allow the system to scale to production workloads.

---

## Author

Mayank Sharma

This project was built as part of an AI / Python Intern screening assignment.

The focus was on:

* Correct system behavior
* Clean API design
* Handling edge cases
* Practical implementation
