import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, Process
from crewai import LLM
from agents import create_agents
from tasks import create_tasks
from database import Database

# Load environment variables
load_dotenv()
llm = LLM(
            model="groq/llama-3.3-70b-versatile",
            temperature=0.7
        )
        
class PromptEngineeringCrew:
    def __init__(self):
        # Check for API key
        if not os.environ.get("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize the Groq LLM with Llama 3.3
        self.llm = LLM(
            model="groq/llama-3.3-70b-versatile",
            
            temperature=0.7
        )
        
        # Initialize database
        self.db = Database()
        
        # Create agents
        self.research_agent, self.prompt_designer_agent, self.evaluation_agent = create_agents(self.llm)
        
    def optimize_prompt(self, user_query):
        """Process a user query through the research, prompt design, and evaluation agents"""
        # Create tasks for the agents
        tasks = create_tasks(
            self.research_agent, 
            self.prompt_designer_agent,
            self.evaluation_agent,
            user_query,
            template_library=self.db
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[self.research_agent, self.prompt_designer_agent, self.evaluation_agent],
            tasks=tasks,
            verbose=True,
            process=Process.sequential,  # Ensure tasks run in sequence
            llm=llm
        )
        
        # Execute the crew's plan
        result = crew.kickoff()
        
        # Save results to database
        try:
            # Extract the string content from TaskOutput objects
            # Fix: Use the proper way to access the string content
            research_output = str(tasks[0].output) if tasks[0].output else "No research output available"
            prompt_output = str(tasks[1].output) if tasks[1].output else "No prompt output available"
            evaluation_output = str(tasks[2].output) if tasks[2].output else "No evaluation output available"
            
            # Save to database
            query_id = self.db.save_query_results(
                user_query=user_query,
                research_output=research_output,
                optimized_prompt=prompt_output,
                evaluation_output=evaluation_output
            )
            
            # Return combined result with query_id for feedback
            return {
                "query_id": query_id,
                "research": research_output,
                "optimized_prompt": prompt_output,
                "evaluation": evaluation_output,
                "summary": result
            }
        except Exception as e:
            print(f"Error saving results: {str(e)}")
            # Still return results even if saving fails
            return {
                "query_id": None,
                "research": str(tasks[0].output) if tasks[0].output else "No research output available",
                "optimized_prompt": str(tasks[1].output) if tasks[1].output else "No prompt output available",
                "evaluation": str(tasks[2].output) if tasks[2].output else "No evaluation output available",
                "summary": result
            }
    
    def save_feedback(self, query_id, effectiveness_rating, clarity_rating, comments):
        """Save user feedback on prompt quality"""
        if query_id:
            self.db.save_feedback(
                query_id=query_id,
                effectiveness_rating=effectiveness_rating,
                clarity_rating=clarity_rating,
                comments=comments
            )
            return True

