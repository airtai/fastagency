from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class InputResponseModel(BaseModel):
    msg: str
    question_id: Optional[UUID] = None
    error: bool = False


class InitiateWorkflowModel(BaseModel):
    user_id: Optional[UUID] = None
    workflow_uuid: UUID
    name: str
    params: dict[str, Any]
