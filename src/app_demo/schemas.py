from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, field_serializer, Field


class McpItem(BaseModel):
    mcp_id: str = Field(..., description="MCP唯一标识")
    mcp_name: str = Field(..., description="MCP名称")
    mcp_desc: str = Field(..., description="MCP描述信息")
    mcp_type: Optional[str] = Field(None, description="MCP类型")
    mcp_json: dict = Field(..., description="MCP的JSON配置内容")
    creator: str = Field(..., description="创建人")
    create_time: Optional[datetime] = Field(None, description="创建时间")
    status: int = Field(0, description="状态（0=草稿，1=发布）")
    updater: Optional[str] = Field(None, description="最后更新人")
    update_time: Optional[datetime] = Field(None, description="最后更新时间")

    @field_serializer("create_time", "update_time")
    def format_datetime(self, v: Optional[datetime]) -> Optional[str]:
        return v.strftime("%Y-%m-%d %H:%M:%S") if v else None

class McpCreate(BaseModel):
    mcp_id: str = Field(..., description="MCP唯一标识")
    mcp_name: str = Field(..., description="MCP名称")
    mcp_desc: str = Field(..., description="MCP描述信息")
    mcp_type: Optional[str] = Field(None, description="MCP类型")
    mcp_json: dict = Field(..., description="MCP的JSON配置内容")
    creator: str = Field(..., description="创建人")
    status: int = Field(0, description="状态（0=草稿，1=发布）")
    updater: Optional[str] = Field(None, description="最后更新人")


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