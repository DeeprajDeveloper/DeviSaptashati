import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

ENV = os.getenv("FLASK_ENV", "dev")
ENV_FILE = f"env/.env.{ENV}"
load_dotenv(ENV_FILE, override=True)

APP_NAME = os.getenv("APP_NAME", "DeviSaptashati")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
DATABASE_URL = os.getenv("DATABASE_URL", fr"{basedir}/database/deviSaptashatiDB.db")
PORT = int(os.getenv("FLASK_PORT", 700))
HOST = '0.0.0.0'
SECRET_KEY = 'L2@G3W4E'

SWAGGER_ENDPOINT = "/api/docs"
SWAGGER_API_URL = f"/swagger.json"
SWAGGER_CONFIG = {
    "app_name": "Devi Saptashati | API Doc",
    "layout": "BaseLayout",  # Options: "BaseLayout", "StandaloneLayout", "Topbar"
    "deepLinking": True,
    "displayOperationId": True,
    "defaultModelsExpandDepth": -1,
    "defaultModelRendering": "model",
}
