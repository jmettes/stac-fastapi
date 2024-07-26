from stac_fastapi.api.app import StacApi

from stac_fastapi.extensions.core import (
    QueryExtension,
)

from stac_fastapi.api.models import create_get_request_model, create_post_request_model

from stac_fastapi.tiledb.core import CoreCrudClient
from stac_fastapi.tiledb.config import TiledbSettings

settings = TiledbSettings()

extensions = [
    QueryExtension(),
]

post_request_model = create_post_request_model(extensions)

api = StacApi(
    settings=settings,
    extensions=extensions,
    client=CoreCrudClient(post_request_model=post_request_model),
    search_get_request_model=create_get_request_model(extensions),
    search_post_request_model=post_request_model,
)
app = api.app

def run():
    """Run app from command line using uvicorn if available."""
    try:
        import uvicorn

        uvicorn.run(
            "stac_fastapi.tiledb.app:app",
            host="0.0.0.0",
            port=7654,
            log_level="info",
            reload=True,
        )
    except ImportError:
        raise RuntimeError("Uvicorn must be installed in order to use command")


if __name__ == "__main__":
    run()