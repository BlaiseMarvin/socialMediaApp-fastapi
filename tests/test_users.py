import pytest
from app import schemas
from app.config import settings
from jose import JWTError,jwt



# def test_root(client):
#     res=client.get("/")
#     # print(res.json().get('message'))
#     assert res.json().get('message') == "Welcome to my API Boys!!!"
#     assert res.status_code==200

def test_create_user(client):
    res=client.post("/users/",json={'email':'hellothere123@gmail.com','password':'password123'})
    # new_user=schemas.UserOut(**res.json())
    # assert new_user.email == 'hellothere123@gmail.com'
    # assert res.status_code == 201
    print(res.json())

def test_login_user(client,test_user):
    res=client.post("/login",data={'username':test_user['email'],'password':test_user['password']})
    # login_res=schemas.Token(**res.json())
    # # print(res.json())
    # payload=jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])

    # id=payload.get("user_id")
    print(res.json())

    # assert id == test_user['id']
    # assert login_res.token_type == "bearer"
    print(res.json())

@pytest.mark.parametrize("email,password,status_code",[
    ("wrongemail@gmail.com","password123",403),
    ("blaisemavin@gmail.com","wrongpassword",403),
    ("wrongemail@gmail.com","wrongpassword",403),
    (None,"password123",422),
    ("blaisemavin@gmail.com",None,422)
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res=client.post("/login",data={'username':email,'password':password})
    print(res.json())
    # assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'



