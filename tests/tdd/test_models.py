def test_model(db_session, member):
    assert member.username
    assert member.avatar
    assert not member.avatar_thumbnail
