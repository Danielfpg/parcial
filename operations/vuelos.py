from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Vuelo
import csv
import os

CSV_FOLDER = "./csv"
VUELO_CSV = os.path.join(CSV_FOLDER, "vuelo.csv")
VUELO_HEADERS = ["id","Comprado ","usuarios", "Origen", "Destino","Fecha", "Reservas"]


async def regenerar_csv(db: AsyncSession):

    result = await db.execute(select(Vuelo))
    VUelos= result.scalars().all()

    os.makedirs(CSV_FOLDER, exist_ok=True)

    with open(VUELO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=VUELO_HEADERS)
        writer.writeheader()
        for vuelo in VUelos:
            writer.writerow({
                "id": vuelo.id,
                "Comprado": vuelo.comprado,
                "Usuarios":vuelo.usuarios,
                "Origen":vuelo.Origen,
                "Destino":vuelo.Destino,
                "Fecha":vuelo.Fecha,
                "Reservar":vuelo.Reservas
            })




async def Create_Vuelo(db: AsyncSession, usuario: Vuelo):
    vuelo = Vuelo(**usuario.dict())
    db.add(vuelo )
    await db.commit()
    await db.refresh(vuelo)

    archivo_existe = os.path.exists(VUELO_CSV)
    with open(VUELO_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=VUELO_HEADERS)
        if not archivo_existe or os.stat(VUELO_CSV).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "id": vuelo.id,
            "Comprado": vuelo.comprado,
            "Usuarios": vuelo.usuarios,
            "Origen": vuelo.Origen,
            "Destino": vuelo.Destino,
            "Fecha": vuelo.Fecha,
            "Reservar": vuelo.Reservas
        })

    return vuelo


async def find_vuelo_Origen(db: AsyncSession, Origen: str):
    origen = Origen.strip()
    result = await db.execute(select(Vuelo))
    vuelos = result.scalars().all()
    for vuelo in vuelos:
        if vuelo.nombre.strip().lower() == origen.lower():
            return vuelo
    return None

async def find_vuelo_destino(db: AsyncSession, Destino: str):
    destino = Destino.strip()
    result = await db.execute(select(Vuelo))
    vuelos = result.scalars().all()
    for vuelo in vuelos:
        if vuelo.nombre.strip().lower() == destino.lower():
            return vuelo
    return None

async def compra_vuelo(db:AsyncSession, Compra: bool):
    compra:Compra.strip()

