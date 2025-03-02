from sqlmodel import SQLModel, create_engine
from fastapi import FastAPI
from app.seed.roles import check_and_seed_roles
from user_routes import router as user_router
from shopify_oauth import router as shopify_oauth
from app.db.db import engine, SessionLocal

app = FastAPI()

# Database URL
DATABASE_URL = "mysql+pymysql://root:9391@127.0.0.1:3306/gaga"  # Use your actual database URL

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables defined in the models (User, ShopifyStore, etc.)
SQLModel.metadata.create_all(engine)
# Include the user and shopify routes
app.include_router(user_router)
app.include_router(shopify_oauth)

@app.get('/')
def home():
    return "Welcome to the Shopify OAuth2.0 FastAPI example!"
