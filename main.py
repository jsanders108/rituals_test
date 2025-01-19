from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel
from crews.q1_crew.q1_crew import Q1Crew


class RitualsFlowState(BaseModel):
    q1_report_results: str = ""


class RitualsGermanyFlow(Flow[RitualsFlowState]):

    @start()
    def q1_analysis(self, q1_data, q1_reasons, q1_question_text):
        print("Generating Q1 analysis")
        result = (
            Q1Crew()
            .crew()
            .kickoff(inputs={"q1_data": q1_data, "q1_reasons": q1_reasons, "q1_question_text": q1_question_text})
        )
        #print("Q1 analysis generated", result.raw)
        self.state.q1_report_results = result.raw
        #print("self.state.q1_report_results:", self.state.q1_report_results)
        return self.state.q1_report_results


def kickoff(q1_data, q1_reasons, q1_question_text):
    rituals_germany_flow = RitualsGermanyFlow()
    return rituals_germany_flow.q1_analysis(q1_data, q1_reasons, q1_question_text)


def plot():
    rituals_germany_flow = RitualsGermanyFlow()
    rituals_germany_flow.plot()


if __name__ == "__main__":
    # Example hardcoded inputs for standalone testing
    sample_q1_data = []
    sample_q1_reasons = []
    sample_q1_question_text = ""
    kickoff(sample_q1_data, sample_q1_reasons, sample_q1_question_text)




'''
q1_data = [
    {
        "country": "Germany",
        "name of person": "Jessica",
        "rating score": 8.0,
        "reason for score": "Very pleasant narrator's voice. It gives a direct feeling of Christmas and the desire to give gifts.",
        "positive reasons": "Festive/Christmas atmosphere; Family/gifting; Pleasant narrator's voice",
        "negative reasons": "none"
    },
    {
        "country": "Germany",
        "name of person": "Nadine",
        "rating score": 8.0,
        "reason for score": "The campaign appeals to me on an emotional level by showing scenes of warm, festively decorated rooms with flickering candles, snow, party glitter, and happy people.",
        "positive reasons": "Emotional/warm feeling; Festive/Christmas atmosphere; Appealing visuals",
        "negative reasons": "none"
    },
    {
        "country": "Germany",
        "name of person": "Michael",
        "rating score": 10.0,
        "reason for score": "It personally speaks to me very much. Successful and positive, as it appears high-quality.",
        "positive reasons": "Emotional/warm feeling; High-quality / luxury feel",
        "negative reasons": "none"
    },
    {
        "country": "Germany",
        "name of person": "Caroline",
        "rating score": 9.0,
        "reason for score": "I like the campaign very much because it conveys luxury, elegance, and a festive Christmas atmosphere (especially through the setting and the use of red colors).",
        "positive reasons": "High-quality / luxury feel; Festive/Christmas atmosphere; Appealing visuals",
        "negative reasons": "none"
    },
    {
        "country": "Germany",
        "name of person": "Luise",
        "rating score": 3.0,
        "reason for score": "I feel the project gets lost in all the surroundings. I don't see what the product can or does.",
        "positive reasons": "none",
        "negative reasons": "Overshadowed environment; Lack of clarity about product"
    },
    {
        "country": "Germany",
        "name of person": "Johannes",
        "rating score": 6.0,
        "reason for score": "It generally looks valuable, but I don't feel very addressed by the setting and characters.",
        "positive reasons": "High-quality / luxury feel",
        "negative reasons": "Not personally relevant"
    },
    {
        "country": "Germany",
        "name of person": "Nina",
        "rating score": 8.0,
        "reason for score": "The campaign looks very professional, festive, and elegant.",
        "positive reasons": "High-quality / luxury feel; Festive/Christmas atmosphere; Appealing visuals",
        "negative reasons": "none"
    },
    {
        "country": "Germany",
        "name of person": "Sonia",
        "rating score": 10.0,
        "reason for score": "Beautiful colors, Christmassy, cozy.",
        "positive reasons": "Emotional/warm feeling; Festive/Christmas atmosphere; Appealing visuals",
        "negative reasons": "none"
    },
    {
        "country": "Germany",
        "name of person": "Silke",
        "rating score": 9.0,
        "reason for score": "I find the advertisement very appealing. It shows that Rituals is very high-quality, and the ad conveys warmth, joy, and the feeling that Rituals is something special.",
        "positive reasons": "Emotional/warm feeling; High-quality / luxury feel; Appealing visuals",
        "negative reasons": "none"
    },
    {
        "country": "Germany",
        "name of person": "Astrid",
        "rating score": 10.0,
        "reason for score": "It creates anticipation for Christmas and gives the feeling of doing everything right with Rituals.",
        "positive reasons": "Emotional/warm feeling; Festive/Christmas atmosphere; Doing everything right",
        "negative reasons": "none"
    },
    {
        "country": "Germany",
        "name of person": "Matthias",
        "rating score": 7.0,
        "reason for score": "I give the overall score of 7. The campaign is harmonious, the color red is striking but not overwhelming. The Rituals brand is well-represented in both social media and outdoor advertising. However, the video is too focused on luxury (almost ostentation), which is not the case in the ad images. The product selection is good but could be more focused. The location of the display is unclear to me.",
        "positive reasons": "Emotional/warm feeling; Appealing visuals; Brand well represented; Good product selection",
        "negative reasons": "Too luxurious / ostentatious; Inconsistent campaign; Lack of product focus; Unclear location"
    },
    {
        "country": "Germany",
        "name of person": "Pamela",
        "rating score": 7.0,
        "reason for score": "Family, gifts, quality time.",
        "positive reasons": "Emotional/warm feeling; Family/gifting",
        "negative reasons": "none"
    }
]

q1_reasons = {
  "positive reasons": {
      "Emotional/warm feeling": 8,
      "Festive/Christmas atmosphere": 6,
      "Appealing visuals (colors, etc.)": 6,
      "High-quality / luxury feel": 5,
      "Family / gifting": 2,
      "Pleasant narrator's voice": 1,
      "Doing everything right": 1,
      "Brand well represented": 1,
      "Good product selection": 1
  },
  "negative reasons": {
      "Overshadowed environment": 1,
      "Lack of clarity about product": 1,
      "Not personally relevant": 1,
      "Too luxurious / ostentatious": 1,
      "Inconsistent campaign": 1,
      "Lack of product focus": 1,
      "Unclear location": 1
  }
}

q1_question_text= """After viewing these advertisements, what score would you give the Rituals campaign as a whole, 
from 1 (very poor) to 10 (excellent)? Please explain your answer."""
'''