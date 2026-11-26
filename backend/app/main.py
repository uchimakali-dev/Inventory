from fastapi import FastAPI
from app.api.v1.enpoints.user import router as user_router

application = FastAPI(title="Inventory Management")

application.include_router(user_router)

@application.get("/")
def home():
    return "welcome"