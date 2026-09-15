from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime


class DashboardStatsResponse(BaseModel):
    total_leads: int
    agent_wise_leads: Dict[str, int]
    status_wise_leads: Dict[str, int]
    source_wise_leads: Dict[str, int]
    category_wise_leads: Dict[str, int]
    recent_leads: List[dict]
    upcoming_followups: List[dict]


class EmployeeDashboardResponse(BaseModel):
    total_leads: int
    my_leads: int
    status_wise_leads: Dict[str, int]
    source_wise_leads: Dict[str, int]
    category_wise_leads: Dict[str, int]
    today_followups: List[dict]
    recent_calls: List[dict]
