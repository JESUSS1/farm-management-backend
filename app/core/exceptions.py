from fastapi import status


class AppException(Exception):
    """Excepción base para errores controlados de la aplicación."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error de la aplicación"

    def __init__(
        self,
        detail: str | None = None,
        status_code: int | None = None,
    ):
        if detail is not None:
            self.detail = detail

        if status_code is not None:
            self.status_code = status_code

        super().__init__(self.detail)


class UserNotFoundException(AppException):
    """Se lanza cuando un usuario no existe."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Usuario no encontrado"


class UsernameAlreadyExistsException(AppException):
    """Se lanza cuando el username ya está registrado."""

    status_code = status.HTTP_409_CONFLICT
    detail = "El nombre de usuario ya está registrado"


class EmailAlreadyExistsException(AppException):
    """Se lanza cuando el correo ya está registrado."""

    status_code = status.HTTP_409_CONFLICT
    detail = "El correo electrónico ya está registrado"


class RoleNotFoundException(AppException):
    """Se lanza cuando el rol del sistema no existe."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "El rol del sistema no existe"


class FarmRoleNotFoundException(AppException):
    """Se lanza cuando el rol de granja no existe."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "El rol de granja no existe"


class FarmRoleAlreadyExistsException(AppException):
    """Se lanza cuando el nombre del rol de granja ya existe en la granja."""

    status_code = status.HTTP_409_CONFLICT
    detail = "El nombre del rol de granja ya está registrado en esta granja"


class FarmRolePermissionNotFoundException(AppException):
    """Se lanza cuando el permiso del rol de granja no existe."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "El permiso del rol de granja no existe"


class FarmRolePermissionAlreadyExistsException(AppException):
    """Se lanza cuando el permiso ya está asignado al rol de granja."""

    status_code = status.HTTP_409_CONFLICT
    detail = "El permiso ya está asignado a este rol de granja"


class FarmNotFoundException(AppException):
    """Se lanza cuando la granja no existe."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "La granja no existe"


class EmptyUpdateException(AppException):
    """Se lanza cuando no se envían campos para actualizar."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Debe enviar al menos un campo para actualizar"


class NullFieldNotAllowedException(AppException):
    """Se lanza cuando un campo obligatorio se intenta actualizar a null."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, field_name: str):
        super().__init__(detail=f"El campo '{field_name}' no puede ser nulo")


class InvalidCredentialsException(AppException):
    """Se lanza cuando el usuario o la contraseña son incorrectos."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Usuario o contraseña incorrectos"


class InactiveUserException(AppException):
    """Se lanza cuando un usuario desactivado intenta autenticarse."""

    status_code = status.HTTP_403_FORBIDDEN
    detail = "El usuario se encuentra desactivado"


class InvalidTokenException(AppException):
    """Se lanza cuando un access token no es válido."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token de acceso inválido"


class ExpiredTokenException(AppException):
    """Se lanza cuando un access token ha expirado."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "El token de acceso ha expirado"


class ForbiddenException(AppException):
    status_code = 403
    detail = "No tienes permisos para realizar esta acción"


class PermissionNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Permiso no encontrado",
        )


class PermissionCodeAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=409,
            detail="El código del permiso ya está registrado",
        )
