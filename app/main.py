from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chatbot, tips, followups, game_overview
from app.utils.error_handler import setup_error_handlers
from app.utils.logger import get_logger
from app.config import settings

# Get logger for main module
logger = get_logger("main")

def create_app() -> FastAPI:
    """
    Application factory function to create and configure the FastAPI app.
    
    Returns:
        A configured FastAPI application
    """
    logger.info("Initializing application...")
    
    # Create FastAPI app
    app = FastAPI(
        title="League of Legends Assistant API",
        description="API for League of Legends game assistance and chatbot",
        version="1.0.0",
    )
    
    # Set up CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routers
    logger.info("Registering API routers...")
    app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
    app.include_router(followups.router, prefix="/suggestions", tags=["Follow-ups"])
    app.include_router(tips.router, prefix="/tips", tags=["Tips"])
    app.include_router(game_overview.router, prefix="/game_overview", tags=["Game Overview"])
    
    # Set up error handlers
    setup_error_handlers(app)
    
    # Root endpoint
    @app.get("/", tags=["Health"])
    def root():
        """
        Root endpoint for API health check.
        """
        return {"status": "ok", "message": "Welcome to the League of Legends Assistant API!"}
    
    logger.info("Application initialization complete")
    return app

# Create the application instance
app = create_app()
