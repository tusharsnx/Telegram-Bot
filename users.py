from database.crud import (
    read_user,
    create_user,
    update_user
)

async def save_income_and_paydate(username, income, pay_date):
    result = await create_user(username=username, income=income, pay_date=pay_date)
    if result:
        return True
    else:
        return False


async def save_mi(username, mi):
    user = await read_user(username=username)
    user.update(dict(mi=mi))
    result = await update_user(username=username, data=user)
    if result:
        return True
    else:
        return False


async def save_me(username, me):
    user = await read_user(username=username)
    user.update(dict(me=me))
    result = await update_user(username=username, data=user)
    if result:
        return True
    else:
        return False


async def get_detail(username):
    user = await read_user(username)
    return user