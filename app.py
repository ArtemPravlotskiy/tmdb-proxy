from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
import httpx
import os

app = FastAPI()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise RuntimeError("TMDB_API_KEY is missing")


@app.get("/proxy")
async def proxy(request: Request, endpoint: str | None = None):
    if not endpoint:
        raise HTTPException(status_code=400, detail="Missing endpoint parameter")

    url = f"https://api.themoviedb.org/3/{endpoint}"
    params = dict(request.query_params)
    params["api_key"] = TMDB_API_KEY

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


@app.get("/image")
async def image_proxy(path: str | None = None):
    if not path:
        raise HTTPException(status_code=400, detail="Missing path parameter")

    url = f"https://image.tmdb.org/t/p/w500{path}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return Response(
        content=response.content,
        media_type=response.headers.get("Content-Type"),
        status_code=response.status_code
    )
