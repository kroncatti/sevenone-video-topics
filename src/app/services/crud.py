from sqlalchemy.orm import Session
from app.models.schema import VideoCreate, VideoResponse
from app.models.db import Video, FeatureVector


# Helper functions. Could be moved somewhere else.
def _get_feature_vector_as_list(db: Session, video_id: int) -> FeatureVector:
    feature_vectors = (
        db.query(FeatureVector)
        .filter(FeatureVector.video_id == video_id)
        .order_by(FeatureVector.feature_index)  # Ensure correct order
        .all()
    )
    return [fv.feature_value for fv in feature_vectors]


def create_video(db: Session, video: VideoCreate) -> Video:
    
    # Wrap everything in a transaction block to avoid partial insertions
    with db.begin():
        # Create Video object
        db_video = Video(
            content_id=video.content_id,
            actual_label=video.actual_label,
            predicted_label=video.predicted_label,
            tvshow=video.tvshow
        )
        db.add(db_video)
        db.flush()

        # Add Feature Vectors
        for index, value in enumerate(video.feature_vector):
            db_feature_vector = FeatureVector(
                video_id=db_video.id,
                feature_index=index,
                feature_value=value
            )
            db.add(db_feature_vector)

    db.commit()
    
    feature_vector_list = _get_feature_vector_as_list(db, db_video.id)
    
    # Return the formatted response
    return VideoResponse(
        content_id=db_video.content_id,
        actual_label=db_video.actual_label,
        predicted_label=db_video.predicted_label,
        tvshow=db_video.tvshow,
        feature_vector=feature_vector_list
    )

def get_video_by_content_id(db: Session, content_id: str) -> Video:
    
    db_video = db.query(Video).filter(Video.content_id == content_id).first()

    if not db_video:
        return None
    
    feature_vector_list = _get_feature_vector_as_list(db, db_video.id)

    # Return the formatted response
    return VideoResponse(
        content_id=db_video.content_id,
        actual_label=db_video.actual_label,
        predicted_label=db_video.predicted_label,
        tvshow=db_video.tvshow,
        feature_vector=feature_vector_list
    )