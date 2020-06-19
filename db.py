import sqlite3
import os
from typing import Tuple, List, Union


class db_Error(Exception):
    pass


conn: sqlite3.Connection
c: sqlite3.Cursor


def open_db() -> int:
    """
        Открытие БД.
        Если БД не существует, будет создана новая БД.
    """
    global conn
    global c

    try:
        
        if os.path.exists(os.path.join('authentication', 'service')):
            conn = sqlite3.connect(os.path.join(
                'authentication', 'service', 'database.db'))
            c = conn.cursor()
        else:
            os.mkdir(os.path.join('authentication', 'service'))
            conn = sqlite3.connect(os.path.join(
                'authentication', 'service', 'database.db'))
            c = conn.cursor()
        return 0
    except sqlite3.Error as e:
        raise db_Error(" " + str(e))


def close_db() -> int:
    global conn
    try:
        conn.close()
        return 0
    except sqlite3.Error as e:
        raise db_Error(" " + str(e))


def create_table() -> int:
    """
        Создание таблицы, если она не существует.
    """
    global conn
    global c

    try:
        with conn:
            c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                login       TEXT        PRIMARY KEY NOT NULL UNIQUE, \
                hash        BLOB        NOT NULL, \
                dir         TEXT        NOT NULL UNIQUE, \
                enc_key     BLOB        NOT NULL, \
                iv          BLOB        NOT NULL
                )
            """)
        return 0
    except sqlite3.Error as e:
        raise db_Error(" " + str(e))


def insert(login: str, hash: bytes, dir: str,
           enc_key: bytes, iv: bytes) -> int:
    global conn
    global c
    if not isinstance(login, str) or not isinstance(hash, bytes) \
            or not isinstance(dir, str) or not isinstance(enc_key, bytes) \
            or not isinstance(iv, bytes):
        raise db_Error("Invalid login type")
    if len(login) < 1:
        raise db_Error("Invalid login length")
    if login == 'None':
        raise db_Error(
            f"You can not use {login} as a login")
    try:
        with conn:
            c.execute("""
                INSERT INTO users (login, hash, dir, enc_key, iv) \
                VALUES (?, ?, ?, ?, ?)""",
                      (login, hash, dir, enc_key, iv))
        return 0
    except sqlite3.IntegrityError as e:
        raise db_Error(" " + str(e))


def cut(login: str) -> int:
    global conn
    global c
    if not isinstance(login, str):
        raise db_Error("Invalid login type")
    if len(login) < 1:
        raise db_Error("Invalid login length")

    with conn:
        c.execute("""SELECT * FROM users WHERE login=?""", (login, ))
        info: Tuple[str, bytes, str, bytes] = c.fetchone()
        if info is None:
            raise db_Error("Invalid login")

    try:
        with conn:
            c.execute("""DELETE FROM users WHERE login=?""", (login, ))
        return 0
    except sqlite3.IntegrityError as e:
        raise db_Error(" " + str(e))


def update(login: str = 'None', hash: bytes = b'None',
           dir: str = 'None', enc_key: bytes = b'None',
           iv: bytes = b'None') -> int:
    global conn
    global c

    if login == 'None':
        raise db_Error("Login not specified")

    try:
        with conn:
            c.execute("""SELECT * FROM users WHERE login=?""", (login, ))
            if c.fetchone() is None:    # type: ignore
                raise db_Error(
                    f"User with login {login} not found")
    except sqlite3.IntegrityError as e:
        raise db_Error(" " + str(e))

    temp_values: List[Union[str, bytes, str, bytes, bytes]] = [
        login, hash, dir, enc_key, iv]
    temp_types: List[type] = [
        str, bytes, str, bytes, bytes]

    for i in range(len(temp_values)):
        if not isinstance(temp_values[i], temp_types[i]):
            raise db_Error("Invalid data type")
        if len(temp_values[i]) < 1:
            raise db_Error("Invalid data length")

    try:
        with conn:
            if hash != b'None':
                c.execute("""
                UPDATE users SET hash=? WHERE login=?""", (hash, login))
            if dir != 'None':
                c.execute("""
                UPDATE users SET dir=? WHERE login=?""", (dir, login))
            if enc_key != b'None':
                c.execute("""
                UPDATE users SET enc_key=? WHERE login=?""", (enc_key, login))
            if iv != b'None':
                c.execute("""
                UPDATE users SET iv=? WHERE login=?""", (iv, login))
        return 0
    except sqlite3.IntegrityError as e:
        raise db_Error(" " + str(e))


def info(login: str) -> Union[Tuple[str, bytes, str, bytes, bytes], None]:
    if not isinstance(login, str):
        raise db_Error("Invalid input type")
    global conn
    global c
    try:
        with conn:
            c.execute("""SELECT * FROM users WHERE login=?""", (login, ))
            info: Tuple[str, bytes, str, bytes, bytes] = c.fetchone()
    except sqlite3.IntegrityError as e:
        raise db_Error(" " + str(e))
    if info is None:
        return None
    if not isinstance(info[0], str) or not isinstance(info[1], bytes) \
            or not isinstance(info[2], str) or not isinstance(info[3], bytes) \
            or not isinstance(info[4], bytes):
        raise db_Error("Invalid output type")
    return info
