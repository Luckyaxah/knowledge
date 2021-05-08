def user_schema(user):
    return {
        'id': user.id,
        'username': user.username
    }

def users_schema(users, current_page):
    return {
        "users":[user_schema(user) for user in users],
        "current_page": current_page,
    }