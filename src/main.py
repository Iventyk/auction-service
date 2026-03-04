from fastapi import FastAPI


def create_application() -> FastAPI:
    """
    Application factory.
    """
    application = FastAPI(
        title="Auction Service",
        version="1.0.0",
    )

    return application


app = create_application()
