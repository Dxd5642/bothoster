import logging
import time
import uuid

from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from settings.setting import ALLOWED_ORIGINS, ALLOWED_HOSTS

logger = logging.getLogger("app")


def setup_middleware(app: FastAPI):
    app.add_middleware(
    CORSMiddleware,
    allow_headers=['Content-Type', 'X-CSRF-Token'],
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )

    @app.middleware("http")
    async def request_logging(request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            logging.exception(
                "Unhandled error | request_id=%s",
                request_id
            )
            raise

        duration = time.perf_counter() - start

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "%s %s | status=%s | duration=%.3fs | request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration,
            request_id
        )

        return response