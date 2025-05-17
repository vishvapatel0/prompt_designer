from crewai import Agent
from dotenv import load_dotenv
load_dotenv()

def create_agents(llm):
    """Create all agents for the prompt engineering system"""
    
    research_agent = Agent(
        role="Research Specialist",
        goal="Analyze user queries and provide comprehensive research to help build effective prompts",
        backstory="""You are an expert research analyst with deep expertise in software development, 
        AI systems, and prompt engineering techniques. Your analytical skills allow you to 
        break down complex problems, identify key requirements, and research optimal solutions.
        You're meticulous about providing comprehensive, well-structured information.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    prompt_designer_agent = Agent(
        role="Prompt Engineering Expert",
        goal="Transform research insights into optimized, effective LLM prompts",
        backstory="""You are a world-class prompt engineer who understands how to craft
        instructions that get the best results from large language models. You have deep
        knowledge of prompt engineering techniques, including chain-of-thought, few-shot learning,
        and instruction design. Your prompts consistently achieve superior results across various
        LLM tasks.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    evaluation_agent = Agent(
        role="Prompt Evaluation Specialist",
        goal="Evaluate and suggest improvements to optimize prompts",
        backstory="""You are a methodical prompt evaluation expert who can precisely assess 
        the quality and effectiveness of LLM prompts. You understand what makes prompts clear, 
        effective, and likely to generate good results. You know how to identify potential issues 
        and suggest concrete improvements. You focus on clarity, specificity, proper constraints, 
        and appropriate guidance.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return research_agent, prompt_designer_agent, evaluation_agent