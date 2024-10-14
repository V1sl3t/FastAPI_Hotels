from datetime import date

from fastapi import HTTPException


class HotBookException(Exception):
    detail = "Неожиданная ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(HotBookException):
    detail = "Объект не найден"


class IncorrectPasswordException(HotBookException):
    detail = "Неверный пароль"


class IncorrectTokenException(HotBookException):
    detail = "Невалидный токен"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class AllRoomsAreBookedException(HotBookException):
    detail = "Все номера забронированы"


class ObjectAlreadyExistsException(HotBookException):
    detail = "Похожий объект уже существует"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Такой пользователь уже существует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class HotBookHTTPException(HTTPException):
    status_code = 500
    detail = None
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(HotBookHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(HotBookHTTPException):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedHTTPException(HotBookHTTPException):
    status_code = 409
    detail = "Все номера забронированы"


class UserEmailAlreadyExistsHTTPException(HotBookHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class IncorrectTokenHTTPException(HotBookHTTPException):
    status_code = 404
    detail = "Невалидный токен"


class UserNotFoundHTTPException(HotBookHTTPException):
    status_code = 404
    detail = "Пользователь с таким email не найден"


class IncorrectPasswordHTTPException(HotBookHTTPException):
    status_code = 404
    detail = "Неверный пароль"