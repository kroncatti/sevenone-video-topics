from fastapi import FastAPI

from app.routes.router import router as api_router


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app


# Starting the App
app = get_app()


# == Healthy check endpoints == #
@app.get("/ping")
async def ping():
    return {"ping": "pong!"}