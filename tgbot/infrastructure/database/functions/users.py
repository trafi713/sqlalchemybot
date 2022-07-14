from sqlalchemy import select, update, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from tgbot.infrastructure.database.models import User, UserTransaction


# create functions with sqlalchemy to manage users
async def add_user(session: AsyncSession, telegram_id, first_name, last_name=None, username=None, role='user'):
    insert_stmt = select(
        User
    ).from_statement(
        insert(
            User
        ).values(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            role=role
        ).returning(User).on_conflict_do_nothing()
    )
    result = await session.scalars(insert_stmt)
    return result.first()


async def get_one_user(session: AsyncSession, **kwargs) -> User:
    statement = select(User).filter_by(**kwargs)
    result: AsyncResult = await session.scalars(statement)
    return result.first()


async def get_some_users(session: AsyncSession, *clauses) -> list[User]:
    statement = select(
        User
    ).where(
        *clauses
    ).order_by(
        User.created_at.desc()
    )
    result: AsyncResult = await session.scalars(statement)
    return result.unique().all()


async def get_count_users(session: AsyncSession, *clauses) -> int:
    statement = select(
        func.count(User.telegram_id)
    ).where(
        *clauses
    )
    result: AsyncResult = await session.scalar(statement)
    return result


async def update_user(session: AsyncSession, *clauses, **values):
    statement = update(
        User
    ).where(
        *clauses
    ).values(
        **values
    )
    await session.execute(statement)


async def change_balance(session: AsyncSession, telegram_id, amount, description=None):
    statement = insert(
        UserTransaction
    ).values(
        user_id=telegram_id,
        amount=amount,
        description=description
    )
    await session.execute(statement)


async def get_balance(session: AsyncSession, telegram_id):
    balance = (func.coalesce(func.sum(UserTransaction.amount), 0))
    statement = select(
        balance
    ).where(
        UserTransaction.user_id == telegram_id
    )
    result: AsyncResult = await session.scalar(statement)
    return result
