import pandas as pd

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from io import StringIO
from fastapi import HTTPException

from app.models.db import Video, FeatureVector

def process_csv(contents: bytes):
    # Decode and read CSV
    data_str = contents.decode("utf-8")
    df = pd.read_csv(StringIO(data_str), sep=';')

    # Ensure the DataFrame has the correct columns
    expected_columns = ['content_id', 'actual_label', 'predicted_label', 'feature_vector', 'tvshow']
    if not all(col in df.columns for col in expected_columns):
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    
    # Convert feature_vector from string to list of floats
    df['feature_vector'] = df['feature_vector'].apply(lambda x: [float(i) for i in x.split(',')])

    return df

def insert_df(db: Session, df: pd.DataFrame) -> None:
    try:
        with db.begin():  # Begin a transaction
            for _, row in df.iterrows():
                # Create Video (Record) object
                db_video = Video(
                    content_id=row['content_id'],
                    actual_label=row['actual_label'],
                    predicted_label=row['predicted_label'],
                    tvshow=row['tvshow']
                )
                db.add(db_video)
                db.flush()  # Flush to get the video_id for FeatureVectors

                # Add Feature Vectors
                feature_vector = (
                    [float(i) for i in row['feature_vector'].split(',')]
                    if isinstance(row['feature_vector'], str)
                    else row['feature_vector']
                )

                for index, value in enumerate(feature_vector):
                    db_feature_vector = FeatureVector(
                        video_id=db_video.id,
                        feature_index=index,
                        feature_value=value
                    )
                    db.add(db_feature_vector)

            db.commit()  # Commit if all records are added successfully

    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=f"Failed to insert records: {str(e)}")