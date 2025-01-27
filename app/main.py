from fastapi import FastAPI, Depends, HTTPException
from app.db.db import engine, Base, get_db
from app.routes.user import router as user_router
from app.routes.protected import router as protected_router
from app.seed.permissions import seed_permissions
from app.seed.rolepermissions import seed_role_permissions
from app.utils.mail import send_test_email
from app.routes.invitation import router as invitation_router
from app.models.role import Role
from app.db.db import SessionLocal
from app.seed.roles import check_and_seed_roles
from app.routes.permission import router as permission_router
from app.routes.role import router as role_router

# Initialize the FastAPI app
app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)



@app.get("/")
def root():
    return 'welcome to fast api'

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
app.include_router(user_router, tags=["User Management"], prefix="/users")
app.include_router(invitation_router, tags=["Invitations Management"])
app.include_router(role_router)
app.include_router(permission_router)

@app.on_event("startup")
async def on_startup():
    db = SessionLocal()
    check_and_seed_roles(db)
    seed_permissions(db)
    seed_role_permissions(db)
    db.close()
    print("App startup complete, roles have been checked and seeded if necessary.")
