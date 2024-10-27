# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["AppListResponse", "Data"]


class Data(BaseModel):
    id: Optional[str] = None

    description: Optional[str] = None

    name: Optional[str] = None


class AppListResponse(BaseModel):
    data: Optional[List[Data]] = None
