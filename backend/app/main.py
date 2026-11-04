from fastapi import FastAPI
from app.routers.images import router as image_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ObjectLens API",
    description="API para deteção de objetos e análise de cores.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ObjectLens API is running!"}

app.include_router(image_router)