from fastapi import FastAPI
from app.routers import auth,otp
from app.database import Base,engine
 


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"Message":"Welcome to Study-Buddy app"}



app.include_router(auth.router)
app.include_router(otp.router)