from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from database.session import init_models
from routers import auth, user


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/v1", tags=["auth"])
app.include_router(user.router, prefix="/v1", tags=["users"])

app.add_middleware(GZipMiddleware)
app.add_middleware(TrustedHostMiddleware)
app.add_middleware(ServerErrorMiddleware, debug=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
