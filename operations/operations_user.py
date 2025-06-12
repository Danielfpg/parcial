from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.future import select
import Usuarios
import csv
import os

CSV_FOLDER = "./csv"
USER_CSV = os.path.join(CSV_FOLDER, "users.csv")
USERS_HEADERS = ["id","Documento ","nombre", "mascota"]


async def regenerar_csv(db: AsyncSession):

    result = await db.execute(select(Usuarios))
    usuarios= result.scalars().all()

    os.makedirs(CSV_FOLDER, exist_ok=True)

    with open(USER_CSV, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=USERS_HEADERS)
        writer.writeheader()
        for usuario in usuarios:
            writer.writerow({
                "id": usuario.id,
                "Documento": usuarios.documento,
                "nombre": usuario.nombre,
                "mascota":usuario.mascota
            })




async def Create_usuario(db: AsyncSession, usuario: Usuarios):
    user = Usuarios(**usuario.dict())
    db.add(user )
    await db.commit()
    await db.refresh(user )

    archivo_existe = os.path.exists(USER_CSV)
    with open(USER_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=USERS_HEADERS)
        if not archivo_existe or os.stat(USER_CSV).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "id": usuario.id,
            "Documento": usuario.documento,
            "nombre": usuario.nombre,
            "mascota": usuario.mascota
        })

    return user


async def find_user_doc(db: AsyncSession, docum: int):
    docum = docum.strip()
    result = await db.execute(select(Usuarios))
    usuarios = result.scalars().all()
    for usuario in usuarios:
        if usuario.nombre.strip().lower() == docum.lower():
            return usuario
    return None

async def modificar_carta_energia(db: AsyncSession, docum: int, datos_actualizados: dict):
    usuario = await find_user_doc(db, docum)
    if not usuario:
        return None

    for key, value in datos_actualizados.items():
        if hasattr(usuario, key) and key != "id":
            setattr(usuario, key, value)

    await db.commit()
    await db.refresh(usuario)
    return usuario

async def kill_user(db: AsyncSession, docum=int):
    user = await find_user_doc(db, docum)
    if not user:
        return None
    await db.delete(user)
    await db.commit()

    return "delte to:",user
