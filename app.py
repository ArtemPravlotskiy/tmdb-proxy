from fastapi import FastAPI, HTTPException
import httpx
import os
from fastapi.responses import Response

app = FastAPI()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise RuntimeError("TMDB_API_KEY is missing")


@app.get("/proxy")
async def proxy(endpoint: str):
    url = f"https://api.themoviedb.org/3/{endpoint}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"api_key": TMDB_API_KEY})

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


@app.get("/image")
async def image_proxy(path: str):
    url = f"https://image.tmdb.org/t/p/w500{path}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return Response(
        content=response.content,
        media_type=response.headers.get("Content-Type"),
        status_code=response.status_code
    )
