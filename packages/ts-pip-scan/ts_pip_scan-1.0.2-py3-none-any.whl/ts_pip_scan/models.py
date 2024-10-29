import os
from typing import Optional

from pydantic import BaseModel

TS_API_URL = "https://api.trustsource.io/v2"

class Config(BaseModel):
    project: str
    module: Optional[str] = None
    apiKey: str
    base_url: str = TS_API_URL
    max_legal_warnings: int = os.environ.get("TS_MAX_LEGAL_WARNINGS", 0)
    max_legal_violations: int = os.environ.get("TS_MAX_LEGAL_VIOLATIONS", 0)
    max_vulnerability_warnings: int = os.environ.get("TS_MAX_VULNERABILITY_WARNINGS", 0)
    max_vulnerability_violations: int = os.environ.get("TS_MAX_VULNERABILITY_VIOLATIONS", 0)
    skip_upload: bool = os.environ.get("TS_SKIP_UPLOAD", False)