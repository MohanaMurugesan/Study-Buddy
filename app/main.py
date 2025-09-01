from fastapi import FastAPI
from app.routers import auth,otp,user,profile
from app.database import Base,engine
from app.schedular import start_scheduler
from contextlib import asynccontextmanager


Base.metadata.create_all(bind=engine)

scheduler = None

@asynccontextmanager
async def lifespan(app : FastAPI):

    global scheduler
    scheduler = start_scheduler()
    
    yield

    if scheduler:
        scheduler.shutdown()
        print("Scheduler stopped")

app = FastAPI(lifespan = lifespan)

@app.get("/")
def home():
    return {"Message":"Welcome to Study-Buddy app"}


app.include_router(auth.router)
app.include_router(otp.router)
app.include_router(user.router)
app.include_router(profile.router)