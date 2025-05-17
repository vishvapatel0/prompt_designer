# Multi-Agent Prompt Engineering System

A sophisticated AI system that transforms simple user queries into optimized, high-quality prompts for Large Language Models (LLMs) using a multi-agent approach with CrewAI and Llama 3.3.

![Prompt Engineering System].

## Overview

This project implements a three-agent AI system that collaborates sequentially to transform basic user queries into expertly crafted prompts:

1. **Research Agent** analyzes the query and provides comprehensive research
2. **Prompt Designer Agent** transforms research into an optimized prompt
3. **Evaluation Agent** assesses the prompt quality and suggests improvements

The system includes a web interface, template library, and feedback collection mechanism to continuously improve prompt quality.

## Features

- **Multi-Agent Processing**: Three specialized AI agents work sequentially to create optimized prompts
- **Template Library**: Pre-built templates for common prompt scenarios
- **Feedback Loop**: Users can rate and comment on generated prompts
- **Web Interface**: Clean, responsive interface to interact with the system
- **Clipboard Integration**: Easy copying of optimized prompts
- **Database Storage**: All queries, results, and feedback stored for future reference

## Technology Stack

- **CrewAI**: Framework for orchestrating multiple AI agents
- **Llama 3.3 (70B)**: Powerful LLM model via Groq API
- **FastAPI**: Backend web framework
- **SQLite**: Database for storing templates, queries, and feedback
- **SQLAlchemy**: ORM for database interactions
- **Jinja2**: HTML templating
- **JavaScript/CSS**: Frontend interface

## Installation

### Prerequisites

- Python 3.8+
- Groq API key (for accessing Llama 3.3)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/prompt-engineering-system.git
   cd prompt-engineering-system
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Access the web interface at http://localhost:8000

3. Enter your query in the input field and click "Generate Optimized Prompt"

4. Review the research, optimized prompt, and evaluation results in the tabs

5. Provide feedback on the prompt quality to help improve the system

## Project Structure

```
prompt-engineering-system/
├── app.py              # FastAPI web application
├── main.py             # PromptEngineeringCrew implementation
├── agents.py           # Agent definitions
├── tasks.py            # Task definitions
├── database.py         # Database interface
├── models.py           # SQLAlchemy models
├── templates/          # HTML templates
│   └── index.html      # Main interface
├── static/             # Static assets
│   ├── styles.css      # CSS styles
│   └── scripts.js      # JavaScript functionality
├── requirements.txt    # Project dependencies
└── .env                # Environment variables (API keys)
```

## How It Works

1. **Query Submission**: User submits a query through the web interface
2. **Research Phase**: Research Agent analyzes the query and creates comprehensive research
3. **Prompt Design**: Prompt Designer Agent uses research to create an optimized prompt
4. **Evaluation**: Evaluation Agent assesses prompt quality and suggests improvements
5. **Results Display**: All outputs are presented to the user through the interface
6. **Feedback Collection**: User can provide ratings and comments on the prompt quality

## Example Use Cases

- Creating complex programming project prompts
- Designing data analysis research questions
- Formulating educational content requirements
- Specifying creative writing scenarios
- Crafting technical documentation outlines

## Future Enhancements

- User authentication system
- A/B testing for multiple prompt variants
- Direct integration with LLM providers for prompt testing
- Machine learning system to improve prompts based on feedback
- Export/import functionality for templates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- CrewAI for the multi-agent framework
- Groq for providing access to Llama 3.3 models
