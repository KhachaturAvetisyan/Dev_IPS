from src.api_server import app
import uvicorn
import json

if __name__ == "__main__":
    # Read config file
    configs = json.load(open("configs/configs.json"))

    # Run the API server
    uvicorn.run(app, host=configs["api_server"]["host"], port=configs["api_server"]["port"])
