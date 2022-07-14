from typing import List

from sqlalchemy import Column, VARCHAR, BIGINT, ForeignKey, DECIMAL, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from tgbot.infrastructure.database.models.base import TimeStampMixin, DatabaseModel


class User(DatabaseModel, TimeStampMixin):
    telegram_id = Column(BIGINT, nullable=False, autoincrement=False, primary_key=True)
    first_name = Column(VARCHAR(200), nullable=False)
    last_name = Column(VARCHAR(200), server_default=expression.null(), nullable=True)
    username = Column(VARCHAR(200), server_default=expression.null(), nullable=True)
    role = Column(VARCHAR(20), nullable=False)

    referrer_id = Column(
        BIGINT,
        ForeignKey("users.telegram_id", ondelete="SET NULL", name="FK__users_referrer_id"),
        nullable=True
    )  # id of the user who referred this user

    # Referrer is the user who referred this user
    referrer: "User" = relationship(
        "User",
        back_populates="referrals",
        lazy="joined",
        # uselist=False,
        remote_side=[telegram_id],
        join_depth=1
    )

    # Referrals are the users who were referred by this user
    referrals: List["User"] = relationship(
        "User",
        remote_side=[referrer_id],
        back_populates="referrer",
        lazy="joined",
        join_depth=1,
        order_by='User.created_at.desc()'
    )
    commands: List[str] = relationship('CommandSetting', back_populates='users')


class UserTransaction(DatabaseModel, TimeStampMixin):
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    amount = Column(DECIMAL(19, 2), nullable=False)
    description = Column(VARCHAR(200), nullable=True)
    user_id = Column(BIGINT, ForeignKey("users.telegram_id", ondelete="CASCADE", name="FK__transactions_user_id"),
                     nullable=False)
    user: "User" = relationship("User", lazy="joined")
