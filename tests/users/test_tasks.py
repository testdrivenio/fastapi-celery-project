from unittest import mock

import pytest
import requests
from celery.exceptions import Retry

from project.users.factories import UserFactory
from project.users.tasks import task_add_subscribe


def test_post_succeed(db_session, monkeypatch, user):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    task_add_subscribe(user.id)

    mock_requests_post.assert_called_with(
        "https://httpbin.org/delay/5",
        data={"email": user.email}
    )


def test_exception(db_session, monkeypatch, user):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    mock_task_add_subscribe_retry = mock.MagicMock()
    monkeypatch.setattr(task_add_subscribe, "retry", mock_task_add_subscribe_retry)

    mock_task_add_subscribe_retry.side_effect = Retry()
    mock_requests_post.side_effect = Exception()

    with pytest.raises(Retry):
        task_add_subscribe(user.id)
