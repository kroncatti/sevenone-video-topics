from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Common base class for all models to allow table creation
Base = declarative_base()


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(String, nullable=False, unique=True)
    actual_label = Column(String, nullable=False)
    predicted_label = Column(String, nullable=False)
    tvshow = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), server_default=text('now()'))

    # Establish a relationship to the FeatureVector table
    feature_vectors = relationship('FeatureVector', back_populates='video', cascade="all, delete-orphan")


class FeatureVector(Base):
    __tablename__ = "feature_vectors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('videos.id', ondelete='CASCADE'), nullable=False)
    feature_index = Column(Integer, nullable=False) # Used to maintain order/sorting for the feature vector
    feature_value = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), server_default=text('now()'))

    # Establish a relationship to the Video table
    video = relationship('Video', back_populates='feature_vectors')
    