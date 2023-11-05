from fastapi import FastAPI
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.routers import auth

app = FastAPI()

app.include_router(auth.router, prefix="/v1", tags=["v1"])

app.add_middleware(GZipMiddleware)
app.add_middleware(TrustedHostMiddleware)
app.add_middleware(ServerErrorMiddleware, debug=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)