import os
import sys

from dotenv import load_dotenv
import pymysql


load_dotenv()

DB_USER = os.getenv("DB_USER", "").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "").strip()
DB_HOST = os.getenv("DB_HOST", "localhost").strip()
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "alojamientos_db").strip()
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4").strip()

errores = []
if not DB_USER:
    errores.append(
        "DB_USER no esta definida. Asegúrate de configurarla en tu archivo .env"
    )
if not DB_NAME:
    errores.append(
        "DB_NAME no esta definida. Asegúrate de configurarla en tu archivo .env"
    )

if errores:
    print("\nError de configuracion de base de datos:", file=sys.stderr)
    for error in errores:
        print(f"  - {error}", file=sys.stderr)
    print(file=sys.stderr)
    sys.exit(1)

print(f'Conectando a MySQL en {DB_HOST}:{DB_PORT} como usuario "{DB_USER}"...')

try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset=DB_CHARSET,
    )

    with connection.cursor() as cursor:
        sql = (
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            f"CHARACTER SET {DB_CHARSET} "
            f"COLLATE {DB_CHARSET}_unicode_ci;"
        )
        cursor.execute(sql)
        connection.commit()

    print(f"Base de datos '{DB_NAME}' creada (o ya existia).")

except pymysql.MySQLError as e:
    print(f"Error al crear la base de datos: {e}", file=sys.stderr)
    sys.exit(1)
finally:
    if "connection" in dir() and connection.open:
        connection.close()
