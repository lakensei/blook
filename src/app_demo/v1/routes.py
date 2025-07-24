import logging

from fastapi import APIRouter, Depends, Path, Query

from src.common.core.response import PaginatedRes
from src.common.core.database.repositories import Repository
from src.infrastructure.database import get_repository
from src.common.deps import get_current_user, CurrentUser
from src.common.core.exceptions import ServiceException
from ..models import Mcp
from ..schemas import McpItem, MCPServerMetadataRequest, MCPServerMetadataResponse, McpCreate
from ..utils import load_mcp_tools
from ...common.helpers.page_helper import paginate

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/mcp", response_model=PaginatedRes[McpItem])
async def mcp_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="一页大小"),
        # session: AsyncSession = Depends(get_db_session),
        repo: Repository[Mcp] = Depends(get_repository),
        user: CurrentUser = Depends(get_current_user)
    ):
        """
        mcp列表
        """
        creator = user.user_id
        crud = repo.get_crud(Mcp)
        logger.debug(f"McpItem fields: {McpItem.model_fields}")
        logger.debug(f"McpItem fields set: {McpItem.model_fields_set}")
        res = await paginate(
            crud,
            page=page,
            page_size=page_size,
            fields=McpItem.model_fields.keys()
        )
        return res

@router.post("/mcp", response_model=McpCreate)
async def mcp_create(
        item: McpCreate,
        # session: AsyncSession = Depends(get_db_session)
        repo: Repository[Mcp] = Depends(get_repository)
    ):
    """
    创建MCP
    """
    crud = repo.get_crud(Mcp)
    item = await crud.create(item.model_dump(exclude_unset=True))
    return item

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