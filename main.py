from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import random

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Existing endpoints
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Random meme endpoint
@app.get("/meme")
async def get_random_meme():
    async with httpx.AsyncClient() as client:
        try:
            # GIPHY API endpoint for trending GIFs
            response = await client.get(
                "https://api.giphy.com/v1/gifs/trending",
                params={"api_key": "A5d47snFXb4KUCaGiWwaawkOKdiWqmjh", "limit": 50}
            )
            response.raise_for_status()
            data = response.json()
            if not data["data"]:
                raise HTTPException(status_code=404, detail="No memes found")
            # Pick a random meme from the response
            meme = random.choice(data["data"])
            return {
                "title": meme["title"],
                "url": meme["images"]["original"]["url"],
                "source": "GIPHY"
            }
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=502, detail="Failed to fetch meme from GIPHY")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")