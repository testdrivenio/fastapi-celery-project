import os

from PIL import Image

from project.tdd.models import Member
from project.tdd.tasks import generate_avatar_thumbnail


def test_task_generate_avatar_thumbnail(db_session, settings, member):
    # init state
    assert member.avatar
    assert not member.avatar_thumbnail

    generate_avatar_thumbnail(member.id)
    member = db_session.query(Member).get(member.id)

    assert member.avatar_thumbnail

    thumbnail_full_path = os.path.join(
        settings.UPLOADS_DEFAULT_DEST,
        member.avatar_thumbnail
    )
    im = Image.open(thumbnail_full_path)

    assert im.height == 100
    assert im.width == 100
