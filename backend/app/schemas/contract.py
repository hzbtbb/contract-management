from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContractBase(BaseModel):
    name: str
    amount: float
    department: str
    party_a: str
    party_b: str
    signing_date: datetime
    execution_start_date: datetime
    execution_end_date: datetime

class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    department: Optional[str] = None
    party_a: Optional[str] = None
    party_b: Optional[str] = None
    signing_date: Optional[datetime] = None
    execution_start_date: Optional[datetime] = None
    execution_end_date: Optional[datetime] = None

class ContractResponse(ContractBase):
    id: int
    file_path: str
    file_type: str
    uploader_id: int
    uploader_name: str
    download_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_contracts: int
    total_amount: float
    department_stats: dict
