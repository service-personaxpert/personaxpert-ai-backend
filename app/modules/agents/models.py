# app/agents/models.py

from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
import datetime
from uuid import uuid4

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    objective = Column(String, nullable=False)
    keywords = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    tone_of_voice = Column(String, nullable=False)
    content_style = Column(String, nullable=False)
    theme = Column(String, nullable=False)
    call_to_action = Column(String, nullable=False)
    age_group = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    search_results = Column(Text, nullable=False)  # Store search results as a JSON string

    blog_suggestions = relationship("BlogSuggestion", back_populates="campaign")

class BlogSuggestion(Base):
    __tablename__ = 'blog_suggestions'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    campaign_id = Column(String, ForeignKey('campaigns.id'), nullable=False)
    idea = Column(Text, nullable=False)
    title = Column(String, nullable=False)
    search_results = Column(Text, nullable=False)  # Store search results as a JSON string
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    campaign = relationship("Campaign", back_populates="blog_suggestions")
    blog_sections = relationship("BlogSection", back_populates="blog_suggestion")

class BlogSection(Base):
    __tablename__ = 'blog_sections'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    blog_suggestion_id = Column(String, ForeignKey('blog_suggestions.id'), nullable=False)
    title = Column(String, nullable=False)
    position = Column(Integer, nullable=False)

    blog_suggestion = relationship("BlogSuggestion", back_populates="blog_sections")
    blog_contents = relationship("BlogContent", back_populates="blog_section")

class BlogContent(Base):
    __tablename__ = 'blog_contents'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    blog_section_id = Column(String, ForeignKey('blog_sections.id'), nullable=False)
    content = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    blog_section = relationship("BlogSection", back_populates="blog_contents")
