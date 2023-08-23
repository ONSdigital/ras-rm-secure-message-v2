import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

from secure_message_v2.models import models


@pytest.fixture(autouse=True)
def seed_db(app_with_db_session, thread):
    app_with_db_session.db.session.add(thread)
    app_with_db_session.db.session.commit()
    yield

    app_with_db_session.db.session.query(models.Thread).delete()
    app_with_db_session.db.session.commit()


@pytest.fixture(scope="session")
def app_with_db_session(app):
    app.db = create_engine("sqlite://")
    models.Base.metadata.create_all(app.db)
    app.db.session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=app.db, expire_on_commit=False)
    )
    app.db.session.execute(text("PRAGMA foreign_keys = ON;"))
    return app
