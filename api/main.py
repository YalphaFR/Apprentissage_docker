from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import redis
import os
import string
import random

app = FastAPI()

# Redis connection
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# Allowed characters for short codes
ALLOWED_CHARS = string.ascii_letters + string.digits
CODE_LENGTH = 6

# Pydantic model for POST /shorten
class URLRequest(BaseModel):
    url: str

# Health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Function to generate a unique short code
def generate_unique_code():
    for _ in range(10):  # essais pour éviter collision
        code = ''.join(random.choices(ALLOWED_CHARS, k=CODE_LENGTH))
        if not r.exists(code):
            return code
    raise Exception("Could not generate unique code")

# POST /shorten
@app.post("/shorten", status_code=201)
async def shorten_url(req: Request):
    try:
        data = await req.json()
    except:
        raise HTTPException(status_code=400, detail={"error": "Invalid JSON"})

    if "url" not in data:
        raise HTTPException(status_code=400, detail={"error": "Missing 'url' field"})

    url = data["url"]
    if not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(status_code=400, detail={"error": "Invalid URL format"})

    # Génération d’un code unique
    short_code = generate_unique_code()
    r.set(short_code, url)

    return {
        "short_code": short_code,
        "short_url": f"http://localhost:8080/{short_code}"
    }

# GET /{code} - redirect
@app.get("/{code}")
def redirect_code(code: str):
    url = r.get(code)
    if not url:
        raise HTTPException(status_code=404, detail={"error": "Short code not found"})
    # RedirectResponse renvoie automatiquement 302 et le header Location
    return RedirectResponse(url=url)