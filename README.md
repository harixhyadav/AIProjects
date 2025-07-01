# Vehicle History API

This repository provides a sample backend service using **FastAPI** and **MongoDB** for a vehicle history report application.

## Features

- `/vehicle/check` POST endpoint to fetch vehicle details by registration number.
- MongoDB integration via the asynchronous `motor` driver.
- Pydantic models for request and response validation.
- Owner name masking (e.g. `Rahul` -> `R****`).
- Swagger UI available at `/docs` when the server is running.
- Sample data insertion script.

## Requirements

- Python 3.8+
- MongoDB instance

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

1. Configure the MongoDB connection string in `backend/main.py` (default is `mongodb://localhost:27017`).
2. Start the server:

```bash
uvicorn backend.main:app --reload
```

## Inserting Sample Data

Run the sample data script to insert a vehicle document for testing:

```bash
python backend/sample_data.py
```

## Checking a Vehicle

Send a POST request to `http://localhost:8000/vehicle/check` with JSON body:

```json
{
  "rc_number": "MH12AB1234"
}
```

A successful response returns masked owner name and other details, while an unknown RC number returns a 404 error.
