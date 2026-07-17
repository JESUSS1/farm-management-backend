from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Genera el hash de una contraseña.
    """
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña coincide con el hash almacenado.
    """
    return password_hash.verify(password, hashed_password)