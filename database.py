from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Base, PromptTemplate, QueryHistory, PromptFeedback

class Database:
    def __init__(self, db_url='sqlite:///prompt_engineering.db'):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)
        
        # Initialize with default templates if DB is empty
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """Initialize DB with some default templates if empty"""
        session = self.SessionLocal()
        template_count = session.query(PromptTemplate).count()
        
        if template_count == 0:
            default_templates = [
                {
                    "category": "data_analysis",
                    "name": "Python Data Processing Script",
                    "description": "Template for creating data processing scripts",
                    "keywords": "python,data,analysis,pandas,matplotlib",
                    "template_text": """Create a Python script for data analysis that performs the following operations:
1. Load and clean the {data_type} data from {source}
2. Perform exploratory data analysis, including statistical summaries and visualizations
3. Apply {analysis_technique} to identify patterns and insights
4. Visualize the results using appropriate charts and graphs
5. Save the processed data and export visualizations

The script should:
- Handle missing values and outliers appropriately
- Be well-documented with comments explaining key steps
- Include error handling for common issues
- Be modular and maintainable with functions for each major operation"""
                },
                {
                    "category": "web_development",
                    "name": "Web Application Architecture",
                    "description": "Template for designing web application architecture",
                    "keywords": "web,frontend,backend,architecture,api",
                    "template_text": """Design a complete architecture for a {application_type} web application that includes:

1. Frontend:
   - Component structure for a {frontend_framework} application
   - State management approach
   - UI/UX considerations and user flow diagrams
   - Responsive design strategies

2. Backend:
   - API design (RESTful or GraphQL) with endpoint specifications
   - Database schema design for {database_type}
   - Authentication and authorization mechanisms
   - Server architecture and deployment considerations

3. Deployment Strategy:
   - CI/CD pipeline description
   - Containerization and orchestration approach
   - Scaling considerations

The architecture should address security concerns, performance optimization, and maintainability."""
                },
                {
                    "category": "machine_learning",
                    "name": "ML Model Development",
                    "description": "Template for machine learning model development",
                    "keywords": "machine learning,model,training,evaluation,deployment",
                    "template_text": """Develop a machine learning solution for {problem_type} that follows these steps:

1. Data Preparation:
   - Data collection strategy for {data_source}
   - Preprocessing pipeline
   - Feature engineering and selection
   - Train/validation/test splitting approach

2. Model Development:
   - Selection and justification of appropriate algorithms
   - Hyperparameter tuning strategy
   - Training process with appropriate regularization
   - Evaluation metrics and validation approach

3. Deployment and Monitoring:
   - Model serialization and deployment strategy
   - Inference optimization
   - Monitoring for drift and performance degradation
   - Retraining strategy

The solution should address potential biases, explain model decisions where appropriate, and consider computational efficiency."""
                }
            ]
            
            for template_data in default_templates:
                template = PromptTemplate(
                    category=template_data["category"],
                    name=template_data["name"],
                    description=template_data["description"],
                    keywords=template_data["keywords"],
                    template_text=template_data["template_text"]
                )
                session.add(template)
            
            session.commit()
        
        session.close()
    
    def get_relevant_templates(self, query, limit=3):
        """Find templates relevant to the given query"""
        session = self.SessionLocal()
        
        # Extract keywords from the query (simplified approach)
        query_words = set(query.lower().split())
        relevant_templates = []
        
        try:
            # Search for templates with matching keywords
            templates = session.query(PromptTemplate).all()
            
            # Score templates based on keyword matches
            scored_templates = []
            for template in templates:
                if template.keywords:
                    template_keywords = set(k.lower().strip() for k in template.keywords.split(','))
                    matches = len(query_words.intersection(template_keywords))
                    if matches > 0:
                        scored_templates.append((template, matches))
            
            # Sort by match score and take top results
            scored_templates.sort(key=lambda x: x[1], reverse=True)
            relevant_templates = [t[0].template_text for t in scored_templates[:limit]]
            
            return relevant_templates
        finally:
            session.close()
    
    def save_query_results(self, user_query, research_output, optimized_prompt, evaluation_output):
        """Save query results to database"""
        session = self.SessionLocal()
        
        query_record = QueryHistory(
            user_query=user_query,
            research_output=research_output,
            optimized_prompt=optimized_prompt,
            evaluation_output=evaluation_output
        )
        
        session.add(query_record)
        session.commit()
        query_id = query_record.id
        session.close()
        
        return query_id
    
    def save_feedback(self, query_id, effectiveness_rating, clarity_rating, comments):
        """Save user feedback for a prompt"""
        session = self.SessionLocal()
        
        feedback = PromptFeedback(
            query_id=query_id,
            effectiveness_rating=effectiveness_rating,
            clarity_rating=clarity_rating,
            comments=comments
        )
        
        session.add(feedback)
        session.commit()
        session.close()