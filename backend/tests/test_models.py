import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Comment, ErrorRecord, Like, Report, StudyRecord, TodoItem, User


def make_user(db, email="a@example.com", nickname="tester"):
    user = User(email=email, password_hash="hash", nickname=nickname)
    db.add(user)
    db.commit()
    return user


def test_all_tables_are_created(engine):
    from sqlalchemy import inspect

    tables = set(inspect(engine).get_table_names())
    assert {
        "users",
        "study_records",
        "todo_items",
        "error_records",
        "comments",
        "likes",
        "reports",
    } <= tables


def test_new_records_default_to_private_and_timestamps_are_set(db_session):
    user = make_user(db_session)
    study = StudyRecord(user_id=user.id, title="제목", content="내용")
    todo = TodoItem(user_id=user.id, title="할 일")
    error = ErrorRecord(user_id=user.id, title="오류", content="내용")
    db_session.add_all([study, todo, error])
    db_session.commit()

    assert study.is_public is False
    assert todo.is_public is False and todo.is_done is False
    assert error.is_public is False and error.is_resolved is False and error.solution is None
    assert study.created_at is not None and study.updated_at is not None


def test_user_email_and_nickname_are_unique(db_session):
    make_user(db_session, email="a@example.com", nickname="same")
    db_session.add(User(email="a@example.com", password_hash="h", nickname="other"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    db_session.add(User(email="b@example.com", password_hash="h", nickname="same"))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_comment_must_target_exactly_one_record(db_session):
    user = make_user(db_session)
    study = StudyRecord(user_id=user.id, title="t", content="c")
    db_session.add(study)
    db_session.commit()

    db_session.add(Comment(user_id=user.id, study_record_id=study.id, content="좋아요"))
    db_session.commit()

    db_session.add(Comment(user_id=user.id, content="대상 없음"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    db_session.add(
        Comment(user_id=user.id, study_record_id=study.id, error_record_id=None, content="x")
    )
    db_session.commit()


def test_like_is_unique_per_user_and_record(db_session):
    user = make_user(db_session)
    study = StudyRecord(user_id=user.id, title="t", content="c")
    db_session.add(study)
    db_session.commit()

    db_session.add(Like(user_id=user.id, study_record_id=study.id))
    db_session.commit()

    db_session.add(Like(user_id=user.id, study_record_id=study.id))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_report_is_unique_per_reporter_and_target(db_session):
    user = make_user(db_session)
    db_session.add(Report(reporter_id=user.id, target_type="study_record", target_id=1, reason="이유"))
    db_session.commit()

    db_session.add(Report(reporter_id=user.id, target_type="study_record", target_id=1, reason="또"))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    db_session.add(Report(reporter_id=user.id, target_type="unknown", target_id=1, reason="x"))
    with pytest.raises(IntegrityError):
        db_session.commit()
