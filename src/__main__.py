import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import env
from src.router import post, comment, email
from src.template.tags_metadata import tags_metadata

app = FastAPI(openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router, prefix="/post", tags=['Post'])
app.include_router(comment.router, prefix="/comment", tags=['Comment'])
app.include_router(email.router, prefix="/email", tags=['Email'])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=env.PORT, timeout_keep_alive=60)
