"""
基础设施插件

使用工厂模式根据配置文件动态选择具体实现
在 lifespan 中管理插件的初始化和清理
"""
# dependencies: Dict[str, List[Callable]] = {}
#
# def register_dependency(db_name: str, dependency: Callable):
#     if db_name not in dependencies:
#         dependencies[db_name] = []
#     dependencies[db_name].append(dependency)
#     print(f"Registered dependency for {db_name}")
#
# def get_dependencies(db_name: str) -> List[Callable]:
#     return dependencies.get(db_name, [])


from .manager import InfrastructureManager

__all__ = ["InfrastructureManager"]
