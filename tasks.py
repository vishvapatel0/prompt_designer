from crewai import Task

def create_tasks(research_agent, prompt_designer_agent, evaluation_agent, user_query, template_library=None):
    """Create all tasks for the prompt engineering workflow"""
    
    # Get relevant templates if available
    template_context = ""
    if template_library:
        try:
            relevant_templates = template_library.get_relevant_templates(user_query)
            if relevant_templates:
                template_context = "\n\nRELEVANT TEMPLATES:\n" + "\n\n".join(
                    [f"Template #{i+1}:\n{template}" for i, template in enumerate(relevant_templates)]
                )
        except Exception as e:
            print(f"Error retrieving templates: {str(e)}")
    
    research_task = Task(
        description=f"""Thoroughly analyze the following user query and provide comprehensive research:
        
        USER QUERY: "{user_query}"
        
        Your research must include:
        1. Core problem definition and objectives
        2. Project architecture and key components needed
        3. Recommended libraries, frameworks and tools with rationale
        4. Required functions and algorithms with brief descriptions
        5. Potential challenges and edge cases to consider
        6. Any domain-specific knowledge relevant to the query
        
        Format your research in a clear, structured manner that will be useful for prompt design.
        Be extremely thorough as your research will determine the quality of the final prompt.
        """,
        agent=research_agent,
        expected_output="A comprehensive research report covering all aspects of the user query"
    )
    
    prompt_design_task = Task(
        description=f"""Create an optimized prompt based on the provided research and original user query.
        
        USER QUERY: "{user_query}"
        
        Your optimized prompt should:
        1. Include clear context and background information
        2. Define specific goals and deliverables
        3. Break complex tasks into logical steps
        4. Provide examples or demonstrations where helpful
        5. Include parameters for tone, style, and expertise level
        6. Add guardrails to prevent common errors or hallucinations
        7. Be structured for maximum clarity and effectiveness
        {template_context}
        
        The prompt should be ready to submit to any LLM without further modification.
        Format the final prompt clearly, marking it as "OPTIMIZED PROMPT" at the beginning.
        """,
        agent=prompt_designer_agent,
        expected_output="An optimized LLM prompt based on the research",
        context=[research_task]
    )
    
    evaluation_task = Task(
        description="""Evaluate the optimized prompt and provide an assessment of its quality.
        
        Your evaluation should:
        1. Assess clarity and specificity of instructions
        2. Check if all necessary context is provided
        3. Evaluate the structure and organization of the prompt
        4. Identify any missing elements or potential improvements
        5. Rate the prompt on a scale of 1-10 for effectiveness
        6. Suggest specific improvements if the rating is below 8
        
        Format your evaluation clearly, with a section for strengths, weaknesses, 
        and specific improvement suggestions if needed.
        """,
        agent=evaluation_agent,
        expected_output="A detailed evaluation of the optimized prompt with suggestions for improvement",
        context=[prompt_design_task]
    )
    
    return [research_task, prompt_design_task, evaluation_task]