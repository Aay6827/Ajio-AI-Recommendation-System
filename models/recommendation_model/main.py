# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from recommender import ProductRecommender

app = FastAPI(title="Ajio Recommendation API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize recommender system
recommender = ProductRecommender("products.csv")


@app.get("/")
def root():
    """
    Serve the frontend
    """
    return FileResponse("static/index.html")


@app.get("/products")
def get_products():
    """
    Get all available products
    """
    return {"products": recommender.products["name"].tolist()}


@app.get("/recommend/{product_name}")
def recommend(product_name: str, top_n: int = 3):
    """
    Recommend similar products based on product_name
    """
    recommendations = recommender.recommend(product_name, top_n=top_n)
    return {"product": product_name, "recommendations": recommendations}