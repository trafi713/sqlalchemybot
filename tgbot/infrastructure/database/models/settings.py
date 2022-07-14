from sqlalchemy import Column, ForeignKey, Integer, Boolean, VARCHAR, false
from sqlalchemy.orm import relationship

from tgbot.infrastructure.database.models.base import DatabaseModel, TimeStampMixin


class Command(DatabaseModel, TimeStampMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    command_text = Column(VARCHAR(255), unique=True, nullable=False)
    users = relationship('CommandSetting', back_populates='commands')


class CommandSetting(DatabaseModel, TimeStampMixin):
    command_id = Column(ForeignKey('commands.id'), primary_key=True)
    user_id = Column(ForeignKey('users.telegram_id'), primary_key=True)
    restricted = Column(Boolean, nullable=False, server_default=false())
    commands = relationship('Command', back_populates='users')
    users = relationship('User', back_populates='commands')


class CommandMenu(DatabaseModel, TimeStampMixin):
    command_id = Column(ForeignKey('commands.id'), primary_key=True)
    description = Column(VARCHAR(255), nullable=True)
    in_menu = Column(Boolean, nullable=False, server_default=false())
    lang_code = Column(VARCHAR(2), nullable=True)
