from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Mascotas
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
                "nombre": mascota.nombre,
                "dueño": mascota.duenio,
                "tipo": mascota.tipo,
                "raza":mascota.raza
            })




async def Create_mascota(db: AsyncSession, mascotas: Mascotas):
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
            "nombre": mascota.nombre,
            "dueño": mascota.duenio,
            "tipo": mascota.tipo,
            "raza": mascota.raza
        })

    return mascota


async def find_mascota_id(db: AsyncSession, ID: int):
    id = ID.strip()
    result = await db.execute(select(Mascotas))
    mascotas = result.scalars().all()
    for mascota in mascotas:
        if mascota.nombre.strip().lower() ==id.lower():
            return mascota
    return None

async def modificar_carta_mascota(db: AsyncSession, ID: int, datos_actualizados: dict):
    mascota = await find_mascota_id(db, ID)
    if not mascota:
        return None

    for key, value in datos_actualizados.items():
        if hasattr(mascota, key) and key != "id":
            setattr(mascota, key, value)

    await db.commit()
    await db.refresh(mascota)
    return mascota

async def kill_user(db: AsyncSession, ID: int):
    mascota = await find_mascota_id(db, ID)
    if not mascota:
        return None
    await db.delete(mascota)
    await db.commit()

    return "delte to:", mascota
