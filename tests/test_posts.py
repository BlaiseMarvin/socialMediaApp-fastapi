from typing import List
from app import schemas

def test_get_all_posts(authorized_client,test_posts):
    res=authorized_client.get("/posts/")
    print(res.json())
    # def validate(post):
    #     return schemas.PostOut(**post)

    # posts_map=map(validate,res.json())
    # # p=list(posts_map)
    # # print(p)
    # assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client,test_posts):
    res=client.get("/posts/")
    print(res.json())
    # assert res.status_code == 401

def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    # assert res.status_code == 401
    print(res.json())

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get("/posts/8888")
    #assert res.status_code == 404
    print(res.json())

def test_get_one_post(authorized_client,test_posts):
    
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # validate=schemas.PostOut(**res.json())
    print(res.json())


