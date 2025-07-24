from datetime import datetime
from typing import Optional

from sqlalchemy import String, PrimaryKeyConstraint, SmallInteger, DateTime, text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.impl.sqlalchemy.base import Base


class User(Base):
    __tablename__ = 'sys_user'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='pk_system_users'),
        {'comment': '用户信息表'}
    )

    user_id: Mapped[str] = mapped_column(String(50), primary_key=True, comment='用户ID')
    account: Mapped[str] = mapped_column(String(30), comment='用户账号')
    password: Mapped[str] = mapped_column(String(100), server_default=text("''::character varying"), comment='密码')
    nickname: Mapped[str] = mapped_column(String(30), comment='用户昵称')
    status: Mapped[int] = mapped_column(SmallInteger, server_default=text('0'), comment='帐号状态（0正常 1停用）')
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment='创建时间')
    update_time: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(), comment='更新时间')
    deleted: Mapped[int] = mapped_column(SmallInteger, server_default=text('0'), comment='是否删除')
    remark: Mapped[Optional[str]] = mapped_column(String(500), server_default=text('NULL::character varying'), comment='备注')
    avatar: Mapped[Optional[str]] = mapped_column(String(512), server_default=text("''::character varying"), comment='头像地址')
    login_ip: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("''::character varying"), comment='最后登录IP')
    login_time: Mapped[Optional[datetime]] = mapped_column(DateTime, comment='最后登录时间')
    creator: Mapped[Optional[str]] = mapped_column(String(64), server_default=text("''::character varying"), comment='创建者')
    updater: Mapped[Optional[str]] = mapped_column(String(64), server_default=text("''::character varying"), comment='更新者')