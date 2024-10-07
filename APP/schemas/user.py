def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "mozi_id": item["mozi_id"],
        "name": item["name"],
        "email": item["email"],
        "role":item["role"],
        "created_at": str(item["created_at"]),
        "is_superuser": item["is_superuser"]
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

