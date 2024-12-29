from sqlmodel import SQLModel, create_engine
from fastapi import FastAPI
from user_routes import router as user_router
from shopify_oauth import router as shopify_oauth

app = FastAPI()

# Database URL
DATABASE_URL = "sqlite:///database.db"  # Use your actual database URL

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables defined in the models (User, ShopifyStore, etc.)
SQLModel.metadata.create_all(engine)
# Include the user and shopify routes
app.include_router(user_router)
app.include_router(shopify_oauth)
