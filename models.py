from sqlalchemy import Column, Integer, String, Text, DateTime, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"
    
    id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    template_text = Column(Text, nullable=False)
    keywords = Column(String(500), nullable=True)  # Comma-separated keywords
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "template_text": self.template_text,
            "keywords": self.keywords,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class QueryHistory(Base):
    __tablename__ = "query_history"
    
    id = Column(Integer, primary_key=True)
    user_query = Column(Text, nullable=False)
    research_output = Column(Text, nullable=True)
    optimized_prompt = Column(Text, nullable=True)
    evaluation_output = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_query": self.user_query,
            "research_output": self.research_output,
            "optimized_prompt": self.optimized_prompt,
            "evaluation_output": self.evaluation_output,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class PromptFeedback(Base):
    __tablename__ = "prompt_feedback"
    
    id = Column(Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey('query_history.id'))
    effectiveness_rating = Column(Integer, nullable=True)  # 1-10 scale
    clarity_rating = Column(Integer, nullable=True)  # 1-10 scale
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)