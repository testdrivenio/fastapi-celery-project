import os
from unittest import mock

from project.tdd import tasks
from project.tdd.models import Member


def test_post(client, db_session, settings, member_factory, monkeypatch):
    mock_generate_avatar_thumbnail_delay = mock.MagicMock(name="generate_avatar_thumbnail")
    monkeypatch.setattr(tasks.generate_avatar_thumbnail, "delay", mock_generate_avatar_thumbnail_delay)

    fake_member = member_factory.build()

    avatar_full_path = os.path.join(
        settings.UPLOADS_DEFAULT_DEST,
        fake_member.avatar
    )

    files = {"upload_file": open(avatar_full_path, "rb")}

    data = {
        "username": fake_member.username,
        "email": fake_member.email,
    }

    response = client.post(
        "/tdd/member_signup/",
        data=data,
        files=files,
    )
    assert response.status_code == 200

    member = db_session.query(Member).filter_by(username=fake_member.username).first()
    assert member
    assert member.avatar
    mock_generate_avatar_thumbnail_delay.assert_called_with(
        member.id
    )
