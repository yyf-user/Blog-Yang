from datetime import datetime, date
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ApiStatusCodeBase(BaseModel):
    status_code: int
    count: int


class ApiStatusCodeCreate(ApiStatusCodeBase):
    pass


class ApiStatusCodeUpdate(ApiStatusCodeBase):
    count: Optional[int] = None


class ApiStatusCodeOut(ApiStatusCodeBase):
    id: int
    api_stat_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApiStatBase(BaseModel):
    path: str
    method: str
    calls: int = 0
    avg_response_time: float = 0.0
    error_count: int = 0


class ApiStatCreate(ApiStatBase):
    pass


class ApiStatUpdate(ApiStatBase):
    path: Optional[str] = None
    method: Optional[str] = None
    calls: Optional[int] = None
    avg_response_time: Optional[float] = None
    error_count: Optional[int] = None


class ApiStatOut(ApiStatBase):
    id: int
    last_call: datetime
    error_rate: float
    created_at: datetime
    updated_at: datetime
    status_codes: List[ApiStatusCodeOut] = []

    class Config:
        from_attributes = True


class ApiStatDailyBase(BaseModel):
    date: date
    total_calls: int = 0
    unique_users: int = 0
    avg_response_time: float = 0.0
    error_count: int = 0


class ApiStatDailyCreate(ApiStatDailyBase):
    pass


class ApiStatDailyUpdate(ApiStatDailyBase):
    total_calls: Optional[int] = None
    unique_users: Optional[int] = None
    avg_response_time: Optional[float] = None
    error_count: Optional[int] = None


class ApiStatDailyOut(ApiStatDailyBase):
    id: int
    error_rate: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApiStatsOverview(BaseModel):
    total_calls: int
    unique_users: int
    avg_response_time: float
    error_rate: float
    endpoints: List[Dict] = []


class ApiTrend(BaseModel):
    date: str
    count: int


class ApiDetailOut(BaseModel):
    path: str
    method: str
    calls: int
    avg_response_time: float
    error_rate: float
    last_call: str
    status_codes: Dict[str, int] 