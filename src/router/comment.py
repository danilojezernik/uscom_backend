from fastapi import APIRouter

from src.domain.comment import Comment
from src.services import db

router = APIRouter()


# GET ALL COMMENTS
@router.get("/", operation_id="get_all_comments")
async def get_comments_for_post() -> list[Comment]:
    cursor = db.api.comment.find()
    return [Comment(**document) for document in cursor]


# GET ALL COMMENTS OF A SPECIFIC POST
@router.get("/{post_id}", operation_id="get_comments_of_post")
async def get_comments_for_post_id(post_id: str) -> list[Comment]:
    cursor = db.api.comment.find({'post_id': post_id})
    return [Comment(**document) for document in cursor]


# ADD COMMENT TO A SPECIFIC POST
@router.post("/{post_id}", operation_id="add_comments_to_specific_post")
async def add_comment_to_post(post_id: str, comment: Comment) -> Comment | None:
    comment_dict = comment.dict(by_alias=True)
    comment_dict['post_id'] = post_id

    insert_result = db.api.comment.insert_one(comment_dict)
    if insert_result.acknowledged:
        comment_dict['_id'] = str(insert_result.inserted_id)
        return Comment(**comment_dict)
    return None


# EDIT COMMENT BY ID
@router.put("/{post_id}/{comment_id}", operation_id="edit_comment_by_id")
async def edit_comment(post_id: str, comment_id: str, comment: Comment) -> Comment | None:
    comment_dict = comment.dict(by_alias=True)
    del comment_dict['_id']

    cursor = db.api.comment.update_one({'_id': comment_id, 'post_id': post_id}, {'$set': comment_dict})
    if cursor.modified_count > 0:
        updated_document = db.api.comment.find_one({'_id': comment_id})
        if updated_document:
            updated_document['_id'] = str(updated_document['_id'])
            return Comment(**updated_document)
    return None


# DELETE COMMENT BY ID
@router.delete("/{post_id}/{comment_id}", operation_id="delete_comment_by_id")
async def delete_comment(post_id: str, comment_id: str) -> dict:
    delete_result = db.api.comment.delete_one({'_id': comment_id, 'post_id': post_id})
    if delete_result.deleted_count > 0:
        return {"message": "Comment deleted successfully"}
    else:
        return {"message": "Comment not found"}
