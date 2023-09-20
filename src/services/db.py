from pymongo import MongoClient
from pymongo.database import Database

from src import env
from src.domain.mail import Email
from src.domain.post import Post
from src.domain.comment import Comment

client = MongoClient(env.DB_CONNECTION)
api: Database = client[env.DB_PROCES]

email_seeds = []
post_seeds = []
comment_seeds = []


def init_seeds():
    for i in range(100):
        # Create a post
        post = Post(post_title=f'Harry Potter {i}', author=f'J. K. Rowling {i}')
        post_seeds.append(post.dict(by_alias=True))

        # Create 5 comments for the post
        for j in range(5):
            comment = Comment(post_id=post.id, content=f'Comment {j} for post Harry Potter title {i}', author=f'Danilo Jezernik {j}')
            comment_seeds.append(comment.dict(by_alias=True))

    email = Email(name='Danilo', surname='Jezernik', email='danilo.jezernik@gmail.com', content='Pozdravljen')
    email_seeds.append(email.dict(by_alias=True))


def drop():
    api.comment.drop()
    api.post.drop()
    api.mail.drop()


def seed():
    api.comment.insert_many(comment_seeds)
    api.post.insert_many(post_seeds)
    api.mail.insert_many(email_seeds)


# init_seeds()
drop()
seed()
