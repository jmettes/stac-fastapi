from stac_fastapi.types.config import ApiSettings

class TiledbSettings(ApiSettings):
    """API settings."""
    openapi_url: str = "/openapi.json"