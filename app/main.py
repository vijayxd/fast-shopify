from fastapi import FastAPI, Depends, HTTPException
from app.db.db import engine, Base, get_db
from app.routes.user import router as user_router
from app.routes.protected import router as protected_router
from app.utils.mail import send_test_email
# Initialize the FastAPI app
app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)

@app.get("/test-db")
def test_db_connection(db=Depends(get_db)):
    return {"message": "Database connection is successful!"}


@app.post("/test-email/")
async def test_email(to_email: str):
    result = await send_test_email(to_email)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

app.include_router(protected_router,tags=["User Management"])
app.include_router(user_router, tags=["User Management"])
