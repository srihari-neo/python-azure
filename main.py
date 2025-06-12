from fastapi import FastAPI, HTTPException
import httpx
import random

app = FastAPI()

# Existing endpoints
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# New random meme endpoint
@app.get("/meme")
async def get_random_meme():
    async with httpx.AsyncClient() as client:
        try:
            # GIPHY API endpoint for trending GIFs (no API key needed for public access)
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