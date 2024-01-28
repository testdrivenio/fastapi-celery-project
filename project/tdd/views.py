import os

from fastapi import FastAPI, File, UploadFile, Depends, Form
from sqlalchemy.orm import Session

from . import tdd_router
from project.database import get_db_session
from project.config import settings
from project.tdd.models import Member
from project.tdd.tasks import generate_avatar_thumbnail


@tdd_router.post("/member_signup/")
def member_signup(
        username: str = Form(...),
        email: str = Form(...),
        upload_file: UploadFile = File(...),
        session: Session = Depends(get_db_session)
):
    """
    https://stackoverflow.com/questions/63580229/how-to-save-uploadfile-in-fastapi
    https://github.com/encode/starlette/issues/446
    """
    file_location = os.path.join(
        settings.UPLOADS_DEFAULT_DEST,
        upload_file.filename,
    )
    with open(file_location, "wb") as file_object:
        file_object.write(upload_file.file.read())

    try:
        member = Member(
            username=username,
            email=email,
            avatar=upload_file.filename,
        )
        session.add(member)
        session.commit()
        member_id = member.id
    except Exception as e:
        session.rollback()
        raise

    generate_avatar_thumbnail.delay(member_id)
    return {"message": "Sign up successful"}
