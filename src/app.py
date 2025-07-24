from fastapi import FastAPI

from src.common.core.config import settings, PLUGIN_SETTINGS, LOG_PATH
from src.common.core.logging import setup_logging
from src.infrastructure import InfrastructureManager

# 设置日志
setup_logging(
    log_level=settings.LOG_LEVEL,
    log_dir=LOG_PATH,
    app_name=settings.PROJECT_NAME
)

def register_lifespan():
    """注册周期事件 数据库等插件注册"""
    plugin_manager = InfrastructureManager()
    # 根据配置加载启用的插件

    for plugin_name, plugin_config in PLUGIN_SETTINGS.items():
        if plugin_name not in settings.ENABLED_PLUGINS:
            continue
        if plugin_class := InfrastructureManager.get_plugin_class(plugin_name):
            plugin_manager.register_plugin(plugin_class, plugin_config)
    # 加载插件并配置生命周期
    return plugin_manager.load_plugins()


def register_routers(app_: FastAPI) -> None:
    """注册路由"""
    from src.app_auth import auth_router
    from src.app_demo import demo_router
    app_.include_router(auth_router, tags=["Auth"])
    app_.include_router(demo_router, tags=["Demo"])

    @app_.get("/health")
    async def health_check():
        return {"status": "ok"}


def create_app() -> FastAPI:
    """应用工厂函数"""
    app_ = FastAPI(
        title="BLook",
        description="BLook API",
        version="0.0.1",
        lifespan=register_lifespan()
    )
    # 注册路由
    register_routers(app_)
    return app_


# 创建应用实例
app = create_app()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, log_config=None, port=9100)
