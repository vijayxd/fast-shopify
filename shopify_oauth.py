import json
from pathlib import Path
from fastapi.encoders import jsonable_encoder
import shopify
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from database import get_session
from models import ShopifyStore, User,UpdateProductRequest
from typing import List
import shopify

# Shopify credentials from your Partner Dashboard
SHOPIFY_API_KEY = "da63048e3bbd83a78236a8a350ed70e6"
SHOPIFY_API_SECRET = "3ac631692cdc163047e2013176a068ae"
SHOPIFY_SCOPES = "read_customers,read_orders,read_products,write_orders,write_products"  # Example scopes, you can customize
SHOPIFY_APP_URL = "https://gaga.3djungle.io"  # Your app's URL
VERSION = "2024-07"

router = APIRouter()



shopify.Session.setup(api_key=SHOPIFY_API_KEY, secret=SHOPIFY_API_SECRET)

@router.get("/shopify/authenticate")
async def authenticate_shopify_user(shop:str,state:int):
        newSession = shopify.Session(shop+".myshopify.com", VERSION)
        auth_url = newSession.create_permission_url(SHOPIFY_SCOPES, SHOPIFY_APP_URL+ "/shopify/callback", state)
        return RedirectResponse(auth_url)



@router.get("/shopify/url")
async def login_shopify_user():
        auth_url = "https://admin.shopify.com/admin/oauth/authorize?client_id=da63048e3bbd83a78236a8a350ed70e6&scope=read_customers,read_orders,read_products,write_orders,write_products&state=173486556087900&redirect_uri=https://gaga.3djungle.io/shopify/login"
        return RedirectResponse(auth_url)


@router.get("/shopify/login")
async def authenticate_shopify_user(raw:Request,shop:str, session: Session = Depends(get_session)):
        newSession = shopify.Session(shop, VERSION)
        token = newSession.request_token(raw._query_params) 
        with shopify.Session.temp(shop, VERSION, token):
            return newSession,json.loads(shopify.Shop.current().to_json())
        
@router.get("/shopify/user/{accesstoken}/{shop}")
async def get_shopify_user(shop:str,accesstoken:str, session: Session = Depends(get_session)):

    with shopify.Session.temp(shop, VERSION, accesstoken):
        return shopify.Shop.current().to_json()
    

        
        


@router.get("/shopify/callback")
async def callback_shopify_user(raw:Request,state:int,shop:str, session: Session = Depends(get_session)):
    newSession = shopify.Session(shop+".myshopify.com", VERSION)
    access_token = newSession.request_token(raw._query_params) # request_token will validate hmac and timing attacks
    user = session.get(User, state)
    store = ShopifyStore(user_id=user.id, store_name=shop, access_token=access_token)
    session.add(store)
    try:
        session.commit()
        session.refresh(store)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=e._message())
   
    return store



# Delete Shopify Store
@router.delete("/users/{user_id}/shopify_stores/{store_id}", response_model=ShopifyStore)
def delete_shopify_store(
    user_id: int, store_id: int, session: Session = Depends(get_session)
):
    # Ensure the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the store
    store = session.get(ShopifyStore, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # Ensure the store belongs to the user
    if store.user_id != user_id:
        raise HTTPException(status_code=400, detail="Store does not belong to this user")

    # Delete the store
    session.delete(store)
    session.commit()
    return store

# Get all Shopify Stores for a user
@router.get("/users/{user_id}/shopify_stores/", response_model=List[ShopifyStore])
def get_shopify_stores(user_id: int, session: Session = Depends(get_session)):
    # Ensure the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch all stores for this user
    stores = session.exec(select(ShopifyStore).where(ShopifyStore.user_id == user_id)).all()
    return stores


@router.get("/users/{user_id}/shopify_stores/{store_id}/product/{product_id}")
async def get_product(user_id: int, store_id: int, product_id: int, session: Session = Depends(get_session)):
    # Ensure the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the store
    store = session.get(ShopifyStore, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # Ensure the store belongs to the user
    if store.user_id != user_id:
        raise HTTPException(status_code=400, detail="Store does not belong to this user")

    with shopify.Session.temp(store.store_name, VERSION, store.access_token):

        # Fetch the product from Shopify
        try:
            document = Path("./fullproduct.graphql").read_text().replace("pdid",str(product_id))

            


            product = shopify.GraphQL().execute(query=document)
            
        except shopify.ApiAccessError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")

        return simplify_product_data(json.loads(product))

@router.get("/users/{user_id}/shopify_stores/{store_id}/products")
async def get_products(user_id: int, store_id: int, session: Session = Depends(get_session)):
    # Ensure the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the store
    store = session.get(ShopifyStore, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # Ensure the store belongs to the user
    if store.user_id != user_id:
        raise HTTPException(status_code=400, detail="Store does not belong to this user")

    with shopify.Session.temp(store.store_name, VERSION, store.access_token):
        
        # Fetch all products from Shopify
        try:
           document = Path("./products.graphql").read_text()

           products = shopify.GraphQL().execute(query=document,variables=None,operation_name=None)

            # products = shopify.Product.find(limit=2,fields="id,title,body_html,image.src")
            # productsJSON=[]
            # for product in products:
            #     productsJSON.append(product.to_dict())

        except shopify.ApiAccessError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

        return simplify_shopify_data(json.loads(products))
    
def simplify_shopify_data(data):
    products = []
    for edge in data["data"]["products"]["edges"]:
        node = edge["node"]
        product = {
            "title": node["title"],
            "id": node["id"],
            "variantsCount": node["variantsCount"]["count"],
            "images": [
                media["node"]["preview"]["image"]["url"]
                for media in node["media"]["edges"]
            ],
            "priceRange": {
                "min": {
                    "amount": node["priceRangeV2"]["minVariantPrice"]["amount"],
                    "currency": node["priceRangeV2"]["minVariantPrice"]["currencyCode"]
                },
                "max": {
                    "amount": node["priceRangeV2"]["maxVariantPrice"]["amount"],
                    "currency": node["priceRangeV2"]["maxVariantPrice"]["currencyCode"]
                }
            }
        }
        products.append(product)
    return products

def simplify_product_data(response):
    # Extract the product node
    product = response.get("data", {}).get("product", {})
    
    # Simplify collections
    collections = [
        edge["node"]["title"] for edge in product.get("collections", {}).get("edges", [])
    ]
    
    # Simplify media
    media_urls = [
        edge["node"]["preview"]["image"]["url"] 
        for edge in product.get("media", {}).get("edges", [])
    ]
    
    # Simplify variants
    variants = [
        {
            "price": variant["node"]["price"],
            "id": variant["node"]["id"],
            "displayName": variant["node"]["displayName"],
            "sku": variant["node"]["sku"],
            "image": variant["node"]["image"]["url"] if variant["node"]["image"] else None,
            "options": {
                opt["name"]: opt["value"] 
                for opt in variant["node"].get("selectedOptions", [])
            }
        }
        for variant in product.get("variants", {}).get("edges", [])
    ]
    
    # Simplify product details
    simplified_product = {
        "id": product.get("id", ""),
        "tags": product.get("tags", []),
        "title": product.get("title", ""),
        "productType": product.get("productType", ""),
        "description": product.get("description", ""),
        "collections": collections,
        "media": media_urls,
        "variants": variants,
    }
    
    return simplified_product


@router.patch("/users/{user_id}/shopify_stores/{store_id}/product/{product_id}")
def update_shopify_store(
    payload:UpdateProductRequest,
  product_id:int,  user_id: int, store_id: int, session: Session = Depends(get_session)
):
    # Ensure the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the store
    store = session.get(ShopifyStore, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # Ensure the store belongs to the user
    if store.user_id != user_id:
        raise HTTPException(status_code=400, detail="Store does not belong to this user")
    
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # Ensure the store belongs to the user
    if store.user_id != user_id:
        raise HTTPException(status_code=400, detail="Store does not belong to this user")

    with shopify.Session.temp(store.store_name, VERSION, store.access_token):
        
        try:
            query,variables = build_mutation_query(payload)
            product = shopify.GraphQL().execute(query=query,variables=variables)
            return {"message": product}
        except shopify.ApiAccessError as e:
            raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")






def build_mutation_query(payload: UpdateProductRequest):
    input_fields = []
    variables = {"id": "gid://shopify/Product/"+ payload.product_id}

    # Dynamically add fields to the mutation query
    if payload.title:
        input_fields.append("title: $title")
        variables["title"] = payload.title
    if payload.tags:
        input_fields.append("tags: $tags")
        variables["tags"] = payload.tags
    if payload.product_type:
        input_fields.append("productType: $productType")
        variables["productType"] = payload.product_type
    if payload.collectionsToJoin:
        input_fields.append("collectionsToJoin: $collectionsToJoin")
        variables["collectionsToJoin"] = payload.collectionsToJoin
    if payload.collectionsToLeave:
        input_fields.append("collectionsToLeave: $collectionsToLeave")
        variables["collectionsToLeave"] = payload.collectionsToLeave

    # Construct the mutation query
    query = f"""
    mutation UpdateProductDetails($id: ID!, {', '.join([f'${key}: {value_type}' for key, value_type in [
        ('title', 'String'),
        ('tags', '[String!]'),
        ('productType', 'String'),
        ('collectionsToJoin', '[ID!]'),
        ('collectionsToLeave', '[ID!]'),
    ] if key in variables])}) {{
      productUpdate(input: {{
        id: $id
        {', '.join(input_fields)}
      }}) {{
        product {{
          id
          title
          tags
          productType
          collections(first: 10) {{
            edges {{
              node {{
                id
                title
              }}
            }}
          }}
        }}
        userErrors {{
          field
          message
        }}
      }}
    }}
    """
    return query, variables