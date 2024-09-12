import uvicorn

if __name__ == "__main__":
    config = uvicorn.Config("src.web:init_app", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
