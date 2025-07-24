# # common/db_factory.py
# from contextlib import asynccontextmanager
# from typing import AsyncGenerator
#
#
# from contextvars import ContextVar, Token
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy.ext.asyncio import (
#     AsyncSession,
#     async_sessionmaker,
#     create_async_engine,
# )
#
# from .config import settings
#
# # session_context: ContextVar[str] = ContextVar("session_context")
# #
# #
# # def get_session_context() -> str:
# #     return session_context.get()
# #
# #
# # def set_session_context(session_id: str) -> Token:
# #     return session_context.set(session_id)
# #
# #
# # def reset_session_context(context: Token) -> None:
# #     session_context.reset(context)
#
#
# class DatabaseFactory:
#     _instances = {}
#
#     @classmethod
#     def get_db_session(cls, db_name):
#         if db_name not in cls._instances:
#             cls._instances[db_name] = cls._create_db_session(db_name)
#         return cls._instances[db_name]
#
#     @staticmethod
#     def _create_db_session(db_name):
#         # db_config = getattr(settings, f"DB_{db_name.upper()}_CONFIG")
#         # engine = create_engine(
#         #     f"{db_config['ENGINE']}://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
#         # )
#         engine = create_async_engine(
#             settings.database_configs.get(db_name),
#             echo=False,
#             future=True
#             , pool_recycle=3600
#         )
#
#         async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
#         # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#         return async_session
#
#
# @asynccontextmanager
# async def session_factory(db_name) -> AsyncGenerator[AsyncSession, None]:
#     _session = DatabaseFactory.get_db_session(db_name)()
#     try:
#         yield _session
#     finally:
#         await _session.close()
#
# Base = declarative_base()
# """
# DatabaseFactory.get_db_session('main')
#
# self.db_session.execute
# """
