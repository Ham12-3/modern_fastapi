from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base

class GenerateContent(Base):
    __tablename__ = "generated_contents"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    search_term_id = Column(Integer, ForeignKey("search_terms.id"))
    search_term = relationship("SearchTerm", back_populates="generated_contents")

class SearchTerm(Base):
    __tablename__= "search_terms"

    id= Column(Integer, primary_key=True, index=True)
    term= Column(String, unique=True, index=True)

    generated_contents = relationship("GenerateContent", back_populates="search_term")

    sentiment_analysis = relationship("SentimentAnalysis", back_populates="search_term")


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analyses"
    id= Column(Integer, primary_key=True, index=True)
    readability = Column(String)  # Add this missing column
    sentiment = Column(String)
    search_term_id = Column(Integer, ForeignKey("search_terms.id"))
    search_term = relationship("SearchTerm", back_populates="sentiment_analysis")
