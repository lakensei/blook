import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from uvicorn.logging import DefaultFormatter, AccessFormatter


def setup_logging(
        log_level: str = "INFO",
        log_dir: str = "logs",
        app_name: str = "app"
) -> None:
    """设置日志配置"""
    # 创建日志目录
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # 文件日志格式
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # 控制台日志格式
    console_format = DefaultFormatter(
        '%(asctime)s - %(name)s - %(levelprefix)s - [%(filename)s:%(lineno)d] - %(message)s',
        use_colors=True
    )

    # 访问日志控制台格式
    access_console_format = AccessFormatter(
        '%(asctime)s - %(name)s - %(levelprefix)s - %(client_addr)s - "%(request_line)s" %(status_code)s',
        use_colors=True
    )

    # 创建文件处理器
    file_handler = RotatingFileHandler(
        log_path / f"{app_name}.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_format)

    # 访问日志文件处理器
    access_file_handler = RotatingFileHandler(
        log_path / f"{app_name}_access.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    access_file_handler.setFormatter(file_format)

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)

    # 访问日志控制台处理器
    access_console_handler = logging.StreamHandler(sys.stdout)
    access_console_handler.setFormatter(access_console_format)

    # 清理现有处理器
    for logger_name in ['root', 'uvicorn', 'uvicorn.error', 'uvicorn.access', 'fastapi']:
        logger = logging.getLogger(logger_name) if logger_name != 'root' else logging.getLogger()
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # 配置 Uvicorn 相关日志记录器
    # 一般 Uvicorn 日志
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(numeric_level)
    uvicorn_logger.addHandler(console_handler)
    uvicorn_logger.addHandler(file_handler)
    uvicorn_logger.propagate = False

    # Uvicorn 错误日志（包括启动信息）
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.setLevel(numeric_level)
    uvicorn_error_logger.addHandler(console_handler)
    uvicorn_error_logger.addHandler(file_handler)
    uvicorn_error_logger.propagate = False

    # Uvicorn 访问日志
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.setLevel(numeric_level)
    uvicorn_access_logger.addHandler(access_console_handler)  # 带颜色的访问日志
    uvicorn_access_logger.addHandler(access_file_handler)     # 文件记录
    uvicorn_access_logger.propagate = False

    # FastAPI 日志
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(numeric_level)
    fastapi_logger.addHandler(console_handler)
    fastapi_logger.addHandler(file_handler)
    fastapi_logger.propagate = False