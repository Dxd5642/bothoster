class ServiceException(Exception):
    """Базовое исключение для ошибок бизнес-логики"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)



class InvalidDataForLoginException(ServiceException):
    """Неправильные логин или пароль"""
    pass

class UserAlreadyExistsException(ServiceException):
    """Пользователь с таким логином или email уже существует"""
    pass

class DatabaseException(ServiceException):
    """Ошибка при работе с базод данных"""
    pass

class ServerErrorException(ServiceException):
    """Ошибка в роботе сервера"""
    pass