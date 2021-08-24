from responses.response import (
    start,
    income_and_date,
    mi,
    me,
    show_details,
    close_conversation,
    cancel,
    state_ids
)


states = {
    state_ids["start"]: start,
    state_ids["income_and_date"]: income_and_date,
    state_ids["mi"]: mi,
    state_ids["me"]: me,
    state_ids["show_detail"]: show_details,
    state_ids["close_conversation"]: close_conversation,
    state_ids["cancel"]: cancel
}

active_users = set()
active_users_state = dict()


async def generate_response(text, username):

    # user is active
    if username in active_users:
        state_id = active_users_state[username]
        next_state_id, resp = await states[state_id](text, username)
        if next_state_id==-1:
            active_users.remove(username)
        else:
            active_users_state[username] = next_state_id
        return resp

    # user is not active
    else:
        active_users.add(username)
        next_state_id, resp = await states[0](text, username)
        if next_state_id==-1:
            active_users.remove(username)
        else:
            active_users_state[username] = next_state_id
        return resp