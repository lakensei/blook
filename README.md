# Blook - 可插拔架构 Python 项目模板

一个基于可插拔架构设计的 Python 项目模板，专注于基础设施层的模块化实现。

## 项目结构

```
├── conf/                   # 配置文件目录
│   └── demo.env            # 环境变量配置示例
├── log/                    # 日志文件目录
├── src/                    # 源代码目录
│   ├── app_auth/           # 认证模块demo
│   ├── app_mcp/            # MCP 应用模块demo  (模块下内容多，将routes、models、schemas、services等文件改为目录)
│   ├── common/             # 公共组件
│   ├── components/         # 业务组件
│   ├── infrastructure/     # 基础设施层（可插拔）
│   ├── static/             # 静态文件，只推荐放置离线doc文件
│   ├── tools/              # 工具类
│   ├── app.py              # 应用入口
│   └── __init__.py
└── README.md
```

## 架构设计理念

本项目采用**端口与适配器模式**，将核心业务逻辑与外部依赖解耦：

### 核心原则
- **基础设施可插拔**：所有基础设施组件都可以轻松替换
- **依赖倒置**：业务逻辑依赖抽象，而不是具体实现
- **单一职责**：每个模块只关注自己的核心功能

### Infrastructure 层设计

当前已实现：
- ✅ SQLAlchemy 数据库适配器

未来可扩展：
- 🔄 Redis 缓存适配器


## 快速开始

### 环境配置
```bash
# 复制配置文件
cp conf/demo.env dev.env

# 编辑配置
vim dev.env
```

### 安装依赖
```bash
# 使用uv
uv sync
```

### 启动应用
```bash
# 开发模式
uvicorn src.app:app --reload

# 生产模式
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

## 可插拔架构使用指南

### 插件配置

```bash
.env
# 启用插件 database redis
ENABLED_PLUGINS=["database"]
```

## 扩展新的基础设施组件

```python
# 补充已实现插件
# src/infrastructure/loader.py
class InfrastructureLoader:

    _modules: Dict[str, str] = {
        "sqlalchemy": "src.infrastructure.database.impl.sqlalchemy",
        "milvus": "src.infrastructure.vector.impl.milvus",
        # "tortoise": "src.infrastructure.database.impl.tortoise.register"
    }

# 设置可用插件
# src/infrastructure/manager.py
class InfrastructureManager:
    _available_plugins: Dict[str, Type[InfrastructurePlugin]] = {
        "database": DatabasePlugin,
        "vector": VectorPlugin,
        # "redis": RedisPlugin,
        # "celery": CeleryPlugin
    }
```