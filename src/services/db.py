from pymongo import MongoClient
from pymongo.database import Database

from src import env
from src.domain.post import Post
from src.domain.comment import Comment

client = MongoClient(env.DB_CONNECTION)
api: Database = client[env.DB_PROCES]

post_seeds = []
comment_seeds = []


def init_seeds():
    for i in range(100):
        # Create a post
        post = Post(post_title=f'post_title_{i}', author=f'author_{i}')
        post_seeds.append(post.dict(by_alias=True))

        # Create 5 comments for the post
        for j in range(5):
            comment = Comment(post_id=post.id, content=f'comment_{j} for post {i}', author=f'comment_author_{j}')
            comment_seeds.append(comment.dict(by_alias=True))


def drop():
    api.comment.drop()
    api.post.drop()


def seed():
    api.comment.insert_many(comment_seeds)
    api.post.insert_many(post_seeds)


init_seeds()
drop()
seed()
