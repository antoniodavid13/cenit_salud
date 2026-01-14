from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, cast
from mysql.connector.cursor import MySQLCursorDict

load_dotenv(find_dotenv())

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "cenit_salud_db"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )

def fetch_all_medicos() -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            # Seleccionamos id_medico para que coincida con tu tabla
            cur.execute("SELECT id_medico, nombre, especialidad, correo_interno FROM medicos;")
            return cast(List[Dict[str, Any]], cur.fetchall())
        finally:
            cur.close()
    finally:
        if conn: conn.close()

def insert_medico(nombre: str, especialidad: str, email: str) -> int:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Corregido: Solo 3 placeholders para 3 valores
            cur.execute(
                "INSERT INTO medicos (nombre, especialidad, correo_interno) VALUES (%s, %s, %s)",
                (nombre, especialidad, email)
            )
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn: conn.close()

def delete_medico(medico_id: int) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Corregido: Usar id_medico en el WHERE
            cur.execute("DELETE FROM medicos WHERE id_medico = %s", (medico_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn: conn.close()

def fetch_cliente_by_id(medico_id: int) -> Dict[str, Any] | None:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            # Corregido: especialidad bien escrito e id_medico
            cur.execute(
                "SELECT id_medico, nombre, especialidad, correo_interno FROM medicos WHERE id_medico = %s",
                (medico_id,)
            )
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn: conn.close()

def update_cliente(medico_id: int, nombre: str, especialidad: str, email: str) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Corregido: especialidad bien escrito e id_medico
            cur.execute(
                """
                UPDATE medicos 
                SET nombre = %s, especialidad = %s, correo_interno = %s
                WHERE id_medico = %s
                """,
                (nombre, especialidad, email, medico_id)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn: conn.close()