from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI  # noqa: E402

from app.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION  # noqa: E402
from app.routers import api_router  # noqa: E402


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(api_router, prefix=API_PREFIX)
    return application


app = get_application()
