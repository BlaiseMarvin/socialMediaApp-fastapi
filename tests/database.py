import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db
from app import models


## Setting up the test database


#SQLALCHEMY_DATABASE_URL='postgresql://blaise:DecemberJan1998!@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


# nullified by the fixture
# client = TestClient(app)

@pytest.fixture(scope="function")
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture(scope="function")
def client(session):
    # run code before our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    
    yield TestClient(app)
    # run code after our test finishes