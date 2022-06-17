class CommentDoesNotExistError(Exception):
    message = "评论不存在或已被删除"

    def __str__(self):
        return CommentDoesNotExistError.message
