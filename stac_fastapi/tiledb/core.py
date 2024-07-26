
import attr
from stac_fastapi.types.core import BaseCoreClient
from stac_fastapi.types.stac import Collection, Collections, Item, ItemCollection
from stac_fastapi.types.links import ItemLinks, CollectionLinks
from stac_fastapi.types import stac as stac_types
from stac_fastapi.types.search import BaseSearchPostRequest

from typing import Union, Optional, List, Type

from datetime import datetime
import shapely

import tiledb
import numpy as np
import datetime
import json

NumType = Union[float, int]

BASE_URL = "http://localhost:7654"
COLLECTION_ID = "REMA_32m"

FILE_PATH = "s3://deant-data-public-dev/experimental/rema/rema-32m.tiledb"

config = tiledb.Config()
config["vfs.s3.region"] = "ap-southeast-2"
config["vfs.s3.no_sign_request"] = "true"
ctx = tiledb.Ctx(config)

import os
os.environ["AWS_EC2_METADATA_DISABLED"] = "true"


def create_stac_item(wkb_geometry, shape_id, dem, hillshade):
    geometry = shapely.from_wkb(wkb_geometry.astype(np.uint8).tobytes())
    item = stac_types.Item(
        id=shape_id,
        geometry=shapely.geometry.mapping(geometry),
        bbox=geometry.bounds,
        datetime=datetime.datetime.utcnow(),
        properties={},
        links=ItemLinks(
            collection_id=COLLECTION_ID,
            item_id=shape_id,
            base_url=BASE_URL,
        ).create_links(),
        assets={
            "dem": {
                "href": dem,
                "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                "title": "32m DEM",
                "roles": ["data"],
            },
            "hillshade": {
                "href": hillshade,
                "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                "roles": ["overview", "visual"],
            }
        }
    )

    return item

@attr.s
class CoreCrudClient(BaseCoreClient):

    def all_collections(self, **kwargs) -> Collections:
        """Read all collections from the database."""
        return Collections(
            collections=[
                Collection(
                    id=COLLECTION_ID,
                    title="REMA 32m DEM",
                    description="REMA 32m DEM",
                    links=CollectionLinks(
                        collection_id=COLLECTION_ID,
                        base_url=BASE_URL,
                    ).create_links(),
                )
            ]
        )


    def item_collection(
        self, collection_id: str, limit: int = 10, token: str = None, **kwargs
    ) -> ItemCollection:
        """Read an item collection from the database."""
        pass

    # /collections/asdsadsa/items/27_57_32m_v2.0
    def get_item(self, item_id: str, collection_id: str, **kwargs) -> Item:
        """Get item by item id, collection id."""
        pass

            
    # /search?bbox=96.8173512092876,-65.5945721388298,97.8173512092876,-64.5945721388298
    def get_search(
        self,
        collections: Optional[List[str]] = None,
        ids: Optional[List[str]] = None,
        bbox: Optional[List[NumType]] = None,
        datetime: Optional[Union[str, datetime]] = None,
        limit: Optional[int] = 10,
        query: Optional[str] = None,
        token: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sortby: Optional[str] = None,
        **kwargs,
    ) -> ItemCollection:
        """GET search catalog."""
        xmin, ymin, xmax, ymax = bbox
        with tiledb.open(FILE_PATH, "r", ctx=ctx) as array:
            data = array.query(attrs=["wkb_geometry", "id", "dem", "hillshade"]).multi_index[xmin:xmax, ymin:ymax]
            items = [create_stac_item(wkb_geometry, id, dem, hillshade) for _X, _Y, _Z, wkb_geometry, id, dem, hillshade in zip(*data.values())]
            print(items)

            return ItemCollection(
                type="FeatureCollection",
                features=items,
                numberReturned=len(items),
            )

    # /collections/asdsadsa
    def get_collection(self, collection_id: str, **kwargs) -> Collection:
        """Get collection by id."""
        return {}

    def post_search(
        self, search_request: BaseSearchPostRequest, **kwargs
    ) -> ItemCollection:
        """POST search catalog."""
        pass