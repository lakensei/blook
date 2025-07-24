import logging

from fastapi import APIRouter, Depends, Path, Query

from src.common.core.response import PaginatedRes
from src.infrastructure.database import get_db_session
from src.infrastructure.database.base import AsyncSession
from src.common.deps import get_current_user, CurrentUser
from src.common.core.exceptions import ServiceException
from ..schemas import McpItem, MCPServerMetadataRequest, MCPServerMetadataResponse
from ..services import McpService
from ..utils import load_mcp_tools


logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/mcp", response_model=PaginatedRes[McpItem])
async def mcp_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="一页大小"),
        session: AsyncSession = Depends(get_db_session),
        user: CurrentUser = Depends(get_current_user)
    ):
        """
        mcp列表
        """
        creator = user.user_id
        return await McpService.get_page_list(session, page, page_size)

@router.post("/server/metadata", response_model=MCPServerMetadataResponse)
async def mcp_server_metadata(request: MCPServerMetadataRequest):
    """Get information about an MCP server."""
    try:
        # Set default timeout with a longer value for this endpoint
        timeout = 300  # Default to 300 seconds for this endpoint

        # Use custom timeout from request if provided
        if request.timeout_seconds is not None:
            timeout = request.timeout_seconds

        # Load tools from the MCP server using the utility function
        tools = await load_mcp_tools(
            server_type=request.transport,
            command=request.command,
            args=request.args,
            url=request.url,
            env=request.env,
            timeout_seconds=timeout,
        )

        # Create the response with tools
        response = MCPServerMetadataResponse(
            transport=request.transport,
            command=request.command,
            args=request.args,
            url=request.url,
            env=request.env,
            tools=tools,
            name=request.name
        )

        return response
    except Exception as e:
        logger.exception(f"Error in MCP server metadata endpoint: {str(e)}")
        raise ServiceException()