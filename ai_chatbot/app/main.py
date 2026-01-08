from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.admin import router as admin_router

app = FastAPI(
    title="AI Sales Chatbot",
    description="AI-powered sales chatbot API",
    version="1.0.0"
)

app.include_router(chat_router)
app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    """Redirect root URL to Swagger documentation."""
    return RedirectResponse(url="/docs")