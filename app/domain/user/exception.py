class UserDoesNotExistError(Exception):
    message = "用户不存在或已被删除"

    def __str__(self):
        return UserDoesNotExistError.message


class UserIsAlreadyExistsError(Exception):
    message = "该用户已存在"

    def __str__(self):
        return UserIsAlreadyExistsError.message
