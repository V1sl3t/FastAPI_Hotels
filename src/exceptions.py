class HotBookException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(HotBookException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(HotBookException):
    detail = "Все номера забронированы"


class UserAlreadyExists(HotBookException):
    detail = "Такой юзер уже существует"