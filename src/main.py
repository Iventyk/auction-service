from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions import AuctionError
from src.routers import lots_router, ws_router


def create_application() -> FastAPI:
    application = FastAPI(
        title="Auction Service",
        version="1.0.0",
    )

    @application.exception_handler(AuctionError)
    async def handle_auction_error(
        _: Request, exc: AuctionError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    application.include_router(lots_router)
    application.include_router(ws_router)
    return application


app = create_application()
