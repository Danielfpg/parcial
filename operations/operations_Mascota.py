from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.future import select
import Mascotas
import csv
import os

CSV_FOLDER = "./csv"
PETS_CSV = os.path.join(CSV_FOLDER, "mascotas.csv")
PETS_HEADERS = ["id","nombre", "dueño","tipo_Mascota","raza"]


async def regenerar_csv(db: AsyncSession):

    result = await db.execute(select(Mascotas))
    mascotas= result.scalars().all()

    os.makedirs(CSV_FOLDER, exist_ok=True)

    with open(PETS_CSV, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=PETS_HEADERS)
        writer.writeheader()
        for mascota in mascotas:
            writer.writerow({
                "id": mascota.id,
                "Documento": mascota.documento,
                "nombre": mascota.nombre,
                "mascota":mascota.mascota
            })




async def Create_usuario(db: AsyncSession, mascotas: Mascotas):
    mascota = Mascotas(**mascotas.dict())
    db.add(mascota )
    await db.commit()
    await db.refresh(mascota )

    archivo_existe = os.path.exists(PETS_CSV)
    with open(PETS_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=PETS_HEADERS )
        if not archivo_existe or os.stat(PETS_CSV ).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "id": mascota.id,
            "Documento": mascota.documento,
            "nombre": mascota.nombre,
            "mascota": mascota.mascota
        })

    return mascota


async def find_user_doc(db: AsyncSession, ID: int):
    id = ID.strip()
    result = await db.execute(select(Mascotas))
    mascotas = result.scalars().all()
    for mascota in mascotas:
        if mascota.nombre.strip().lower() == ID.lower():
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
