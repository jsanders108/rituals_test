from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import kickoff

app = FastAPI()

# Define input schema
class CrewAIRequest(BaseModel):
    q1_data: list[dict]
    q1_reasons: dict
    q1_question_text: str

@app.post("/run-analysis/")
async def run_analysis(request: CrewAIRequest):
    try:
        # Validate reasons dictionary keys
        if not all(key in request.q1_reasons for key in ["positive reasons", "negative reasons"]):
            raise HTTPException(status_code=400, detail="'q1_reasons' must contain 'positive reasons' and 'negative reasons' keys.")

        # Call the CrewAI flow
        result = kickoff(request.q1_data, request.q1_reasons, request.q1_question_text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
