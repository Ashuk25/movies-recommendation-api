from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import boto3
from handler.APIHandler import APIHandler
from handler.FetchS3File import FetchS3File
from handler.ReadFile import ReadFile


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

s3_client = boto3.client("s3")

# Your bucket name
bucket_name = "recommended-model-data"

latest_movies_file = FetchS3File.get_latest_file(s3_client, bucket_name, "Movies")
latest_similarity_file = FetchS3File.get_latest_file(s3_client, bucket_name, "Similarity")

# Read and load the pickle files
movies = ReadFile.read_pkl_from_s3(s3_client, bucket_name, latest_movies_file) if latest_movies_file else None
similarity = ReadFile.read_pkl_from_s3(s3_client, bucket_name, latest_similarity_file) if latest_similarity_file else None

# Pydantic model for request body
class MovieRequest(BaseModel):
    movie_name: str

# FastAPI endpoint to get recommendations
@app.post("/recommend/")
def get_recommendations(request: MovieRequest):
    return APIHandler.recommend(movies, similarity, request.movie_name)

# FastAPI endpoint to list all available movies
@app.get("/movies/")
def get_movies():
    return {"movies": movies['title'].tolist()}