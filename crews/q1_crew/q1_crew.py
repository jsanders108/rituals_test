from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
import os
from .q1_quant_analysis_tool import Q1_QuantAnalysisTool



# Now you can access the API key
openai_api_key = os.getenv("OPENAI_API_KEY")
print(openai_api_key)  # For debugging, to see if the correct key is loaded

# Set the LLM to be used
openai_4o = LLM(model="gpt-4o", temperature=0)
openai_4o_mini = LLM(model="gpt-4o-mini", temperature=0)

# The o1 models can't call tools
openai_o1_preview= LLM(model="o1-preview")
openai_o1_mini = LLM(model="o1-mini")

#q1_data_file_path: str = Field(..., description="src\rituals_germany\processed_data\q1_data.json")
#q1_file_reader = FileReadTool(file_path=q1_data_file_path)

#q1_reasons_file_path: str = Field(..., description="src\rituals_germany\processed_data\q1_reasons.json")
#q1_reasons_file_reader = FileReadTool(file_path=q1_reasons_file_path)




@CrewBase
class Q1Crew():
	"""Q1Crew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def q1_quantitative_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['q1_quantitative_analyst'],
			verbose=True,
			allow_delegation=False,
			tools=[Q1_QuantAnalysisTool()],
			llm=openai_4o_mini
		)

	@agent
	def q1_qualitative_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['q1_qualitative_analyst'],
			verbose=True,
			allow_delegation=False,
			llm=openai_4o_mini,
		)

	@agent
	def q1_report_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['q1_report_writer'],
			verbose=True,
			allow_delegation=False,
			llm=openai_4o_mini,
		) 
	

	@task
	def q1_quantitative_task(self) -> Task:
		return Task(
			config=self.tasks_config['q1_quantitative_task'],
		)

	@task
	def q1_qualitative_task(self) -> Task:
		return Task(
			config=self.tasks_config['q1_qualitative_task'],
		)

	@task
	def q1_report_task(self) -> Task:
		return Task(
			config=self.tasks_config['q1_report_task'],	
			output_file='reports\q1_report.md'
		)

 
	@crew
	def crew(self) -> Crew:
		"""Creates the Q1Crew crew"""

		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)
