from crewai.tools import BaseTool
from typing import Type, List, Dict
from pydantic import BaseModel
import json


class Q1_QuantAnalysisInput(BaseModel):
    """Input schema for Q1_QuantAnalysisTool."""
    q1_data: List[Dict]  # A list of dictionaries containing survey data


class Q1_QuantAnalysisTool(BaseTool):
    name: str = "Q1 Quantitative Analysis Tool"
    description: str = (
        "Analyzes Q1 survey rating scores from data and calculates key statistics including "
        "mean, median, and distribution across rating ranges (1-5, 6-8, 9-10)."
    )
    args_schema: Type[BaseModel] = Q1_QuantAnalysisInput

    def _run(self, q1_data: List[Dict]) -> str:
        try:
            # Ensure the data is a list of dictionaries
            if not isinstance(q1_data, list) or not all(isinstance(record, dict) for record in q1_data):
                return "Error: The input data must be a list of dictionaries."

            # Ensure the "rating score" key exists in all records
            if not all("rating score" in record for record in q1_data):
                return "Error: All records in the data must contain a 'rating score' key."

            # Extract non-null rating scores
            scores = [record["rating score"] for record in q1_data if record["rating score"] is not None]

            if not scores:
                return "Error: No valid 'rating score' values found in the data."

            # Calculate statistics
            mean_score = round(sum(scores) / len(scores), 2)
            median_score = sorted(scores)[len(scores) // 2] if len(scores) % 2 != 0 else (
                sorted(scores)[len(scores) // 2 - 1] + sorted(scores)[len(scores) // 2]
            ) / 2

            total_responses = len(scores)
            low_scores = len([score for score in scores if 1 <= score <= 5])
            mid_scores = len([score for score in scores if 6 <= score <= 8])
            high_scores = len([score for score in scores if 9 <= score <= 10])

            pct_low = round((low_scores / total_responses) * 100, 1)
            pct_mid = round((mid_scores / total_responses) * 100, 1)
            pct_high = round((high_scores / total_responses) * 100, 1)

            # Generate results
            results = (
                f"Survey Rating Analysis Results:\n\n"
                f"Basic Statistics:\n"
                f"- Mean Score: {mean_score}\n"
                f"- Median Score: {median_score}\n\n"
                f"Score Distribution:\n"
                f"- Scores 1-5: {pct_low}% ({low_scores} responses)\n"
                f"- Scores 6-8: {pct_mid}% ({mid_scores} responses)\n"
                f"- Scores 9-10: {pct_high}% ({high_scores} responses)\n"
                f"Total Responses: {total_responses}\n\n"
                f"List of scores: {', '.join(map(str, scores))}"
            )

            return results

        except Exception as e:
            return f"Error analyzing survey data: {str(e)}"
