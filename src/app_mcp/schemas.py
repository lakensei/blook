from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, field_serializer, Field


class McpItem(BaseModel):
    """Represents a single MCP item."""
    plan_id: str
    chat_id: str
    creator: str
    status: int
    title: str
    create_time: datetime

    @field_serializer("create_time")
    def format_datetime(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S") if v else None


class MCPServerMetadataRequest(BaseModel):
    """Request model for MCP server metadata."""

    transport: str = Field(
        ..., description="The type of MCP server connection (stdio or sse)"
    )
    command: Optional[str] = Field(
        None, description="The command to execute (for stdio type)"
    )
    args: Optional[List[str]] = Field(
        None, description="Command arguments (for stdio type)"
    )
    url: Optional[str] = Field(
        None, description="The URL of the SSE server (for sse type)"
    )
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables")
    timeout_seconds: Optional[int] = Field(
        None, description="Optional custom timeout in seconds for the operation"
    )


class MCPServerMetadataResponse(BaseModel):
    """Response model for MCP server metadata."""

    transport: str = Field(
        ..., description="The type of MCP server connection (stdio or sse)"
    )
    command: Optional[str] = Field(
        None, description="The command to execute (for stdio type)"
    )
    args: Optional[List[str]] = Field(
        None, description="Command arguments (for stdio type)"
    )
    url: Optional[str] = Field(
        None, description="The URL of the SSE server (for sse type)"
    )
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables")
    tools: List = Field(
        default_factory=list, description="Available tools from the MCP server"
    )
    name: str = Field(None, description="The name of the MCP server")