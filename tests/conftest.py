import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db
from app.oauth2 import create_access_token
from app import models


## Setting up the test database


#SQLALCHEMY_DATABASE_URL='postgresql://blaise:DecemberJan1998!@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

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

@pytest.fixture
def test_user(client):
    user_data={"email":"blaisemavin@gmail.com",
                "password":"password123"}
    res=client.post("/users/",json=user_data)

    new_user=res.json()
    new_user['password']=user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session):
    posts_data=[{
        "title":"first title",
        "content":"first content",
        "owner_id":test_user['id']
    },
    {
        "title":"2nd title",
        "content":"2nd content",
        "owner_id":test_user['id']
    },
    {
        "title":"3rd title",
        "content":"3rd content",
        "owner_id":test_user['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map=map(create_post_model,posts_data)
    posts=list(post_map)

    session.add_all(posts)
    session.commit()

    posts= session.query(models.Post).all()
    return posts

