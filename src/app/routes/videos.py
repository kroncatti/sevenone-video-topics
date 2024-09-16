from fastapi import APIRouter, UploadFile, File, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.schema import VideoCreate, VideoResponse
from app.services import batch
from app.services import crud


router = APIRouter()

@router.post("", name= "Video: create single video", status_code = status.HTTP_201_CREATED, response_model = VideoResponse)
async def post_video(video: VideoCreate, db: Session = Depends(get_db)):
    return crud.create_video(db=db, video=video)

@router.post("/batch/csv", name= "Video: Import CSV batch", status_code=status.HTTP_201_CREATED)
async def post_batch_csv_videos(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()

    # Processing CSV to return a dataframe and inserting it in a db
    df = batch.process_csv(contents)
    batch.insert_df(db=db, df=df)

    return {"message": "success", "count_videos": len(df)}



@router.get("/{content_id}", name= "Video: retrieve single video", status_code = status.HTTP_200_OK, response_model=VideoResponse)
def get_video_by_content_id(content_id: str, db: Session = Depends(get_db)):
    db_video = crud.get_video_by_content_id(db, content_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video