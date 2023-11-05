from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from Utils import utils

# from fastapi.responses import FileResponse


app = FastAPI(
  title="API SMS Whatsapp masivos",
  version="1.0",
  description="Envio masivo de Mensajes por Whatsapp",
  contact={
    "name":"Daniel Calcina",
    "email": "danielnahuncalcinafuentes@gmail.com"
  }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

path_plantilla = "Files/contactos.xlsx"

@app.post("/envio_mensajes/")
async def leer_excel(archivo: UploadFile = File(...)):
    contenido = await archivo.read()
    contacts = pd.read_excel(BytesIO(contenido))
    for index, row in contacts.iterrows():
        contact_nro = '+51'+str(row['nro_celular_contacto']).strip()
        mensaje = f"{str(row['prefijo_mensaje']).strip()} {str(row['nombre_contacto']).strip()} {str(row['sufijo_mensaje']).strip()}"
        utils.enviar_mensaje_instantaneamente(contact_nro, mensaje, tab_close = True, close_time = 1)
    return contacts.to_dict("records")

# @app.get("/obtener-plantilla/")
# async def plantilla():
#     return FileResponse(path_plantilla, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")