from app.core.config import settings
from app.db.database import close_mongo_connection, connect_to_mongo
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()
    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.get("/")
async def health_check():
    return {"service": "history", "status": "healthy", "version": settings.VERSION}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
