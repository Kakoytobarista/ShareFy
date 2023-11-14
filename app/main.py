import logging

from fastapi import FastAPI
from fastapi import Request

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response

from app.routers import auth, user

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def api_logging(request: Request, call_next):
    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    log_message = {
        "host": request.url.hostname,
        "endpoint": request.url.path,
        "response": response_body.decode()
    }
    logger.debug(log_message)
    return Response(content=response_body, status_code=response.status_code,
                    headers=dict(response.headers), media_type=response.media_type)


app.include_router(auth.router, prefix="/v1", tags=["auth"])
app.include_router(user.router, prefix="/v1", tags=["users"])

app.add_middleware(GZipMiddleware)
app.add_middleware(TrustedHostMiddleware)
app.add_middleware(ServerErrorMiddleware, debug=False)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
