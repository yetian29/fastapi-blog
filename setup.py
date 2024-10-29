import uvicorn

from src.web import init_app

if __name__ == "__main__":
    config = uvicorn.Config(init_app, port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
