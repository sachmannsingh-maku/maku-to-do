import uvicorn
from .app.app import create_app
from .app.logging import setup_logging

setup_logging()

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
