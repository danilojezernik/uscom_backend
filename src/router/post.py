from fastapi import APIRouter

from src.domain.post import Post

from src.services import db

router = APIRouter()


# GET ALL POSTS
@router.get("/", operation_id="get_all_posts")
async def get() -> list[Post]:
    cursor = db.api.post.find()
    return [Post(**document) for document in cursor]


# GET POST BY ID
@router.get("/{_id}", operation_id="get_post_by_id")
async def get_id(_id: str) -> Post | dict:
    cursor = db.api.post.find_one({'_id': _id})
    if cursor is None:
        return {"message": "Post does not exist"}
    else:
        return Post(**cursor)


# ADD POST
@router.post("/", operation_id="add_new_post")
async def add_post(post: Post) -> Post | None:
    post_dict = post.dict(by_alias=True)
    insert_result = db.api.post.insert_one(post_dict)
    if insert_result.acknowledged:
        post_dict['_id'] = str(insert_result.inserted_id)
        return Post(**post_dict)
    return None


# EDIT POST BY ID
@router.put("/{_id}", operation_id="edit_post_by_id")
async def edit_post(_id: str, post: Post) -> Post | None:
    post_dict = post.dict(by_alias=True)
    del post_dict['_id']

    cursor = db.api.post.update_one({'_id': _id}, {'$set': post_dict})
    if cursor.modified_count > 0:
        updated_document = db.api.post.find_one({'_id': _id})
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Post(**updated_document)
    return None


# DELETE POST BY ID
@router.delete("/{_id}", operation_id="delete_post_by_id")
async def delete_post(_id: str) -> dict:
    delete_result = db.api.post.delete_one({'_id': _id})
    if delete_result.deleted_count > 0:
        return {"message": "Post deleted successfully"}
    else:
        return {"message": "Post not found"}
