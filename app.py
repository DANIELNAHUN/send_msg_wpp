import os
from io import BytesIO

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from Utils import utils

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

@app.post("/envio_mensajes_personalizados/")
async def mensajes_personalizados(tiempo_espera:int = None ,archivo: UploadFile = File(...)):

    contenido = await archivo.read()

    if tiempo_espera != None and tiempo_espera < 8:
        return "El minimo tiempo de espera entre un mensaje enviado y el siguiente es de 8 segundos, para que Whatsapp no detecte como spam."
    else:
        contacts = pd.read_excel(BytesIO(contenido))
        contacts = contacts.fillna("-")

        lista_correctos=[]
        lista_incorrectos=[]

        for index, row in contacts.iterrows():
            numero = str(row['nro_celular_contacto']).strip()
            pref_msg = str(row['prefijo_mensaje']).strip()
            suf_msg = str(row['sufijo_mensaje']).strip()
            nombre = str(row['nombre_contacto']).strip()

            if numero.isdigit() and numero != "":
                lista_correctos.append(index)

                contact_nro = '+51'+numero

                if pref_msg == "-":
                    pref_msg = "Hola"
                if suf_msg == "-":
                    suf_msg = ""
                if nombre == "-":
                    nombre = ""

                mensaje = f"{pref_msg} {nombre} {suf_msg}"
                tiempo_espera = 8
                utils.enviar_mensaje_instantaneamente(contact_nro, mensaje, tab_close = True, close_time = 1, wait_time = tiempo_espera)

            else:
                lista_incorrectos.append(index)

        return {
            "total": len(contacts),
            "correctos": len(lista_correctos),
            "correctos_data": lista_correctos,
            "incorrectos": len(lista_incorrectos),
            "incorrectos_data": lista_incorrectos,
        }



@app.post("/envio_mensajes_masivos/")
async def mensajes_masivos(msg: str, tiempo_espera:int = None, archivo: UploadFile = File(...)):

    contenido = await archivo.read()

    if tiempo_espera != None and tiempo_espera < 8:
        return "El minimo tiempo de espera entre un mensaje enviado y el siguiente es de 8 segundos, para que Whatsapp no detecte como spam."
    else:
        contacts = pd.read_excel(BytesIO(contenido))
        contacts = contacts.fillna("-")

        lista_correctos=[]
        lista_incorrectos=[]

        for index, row in contacts.iterrows():
            numero = str(row['nro_celular_contacto']).strip()

            if numero.isdigit() and numero != "":
                lista_correctos.append(index)

                contact_nro = '+51'+numero

                mensaje = msg

                tiempo_espera = 8
                utils.enviar_mensaje_instantaneamente(contact_nro, mensaje, tab_close = True, close_time = 1, wait_time = tiempo_espera)

            else:
                lista_incorrectos.append(index)

        return {
            "total": len(contacts),
            "correctos": len(lista_correctos),
            "correctos_data": lista_correctos,
            "incorrectos": len(lista_incorrectos),
            "incorrectos_data": lista_incorrectos,
        }

@app.post("/envio-imagenes/")
async def envio_imagenes_masivos(msg: str, tiempo_espera:int = None, archivo: UploadFile = File(...)):

    if tiempo_espera != None and tiempo_espera < 8:
        return "El minimo tiempo de espera entre un mensaje enviado y el siguiente es de 8 segundos, para que Whatsapp no detecte como spam."
    else:
        # Define la ruta donde se guardará el archivo
        upload_path = "/uploads"
        # Crea la ruta si no existe
        os.makedirs(upload_path, exist_ok=True)
        # Define la ruta completa del archivo
        file_path = os.path.join(upload_path, archivo.filename)
        # Guarda el archivo en la ruta especificada
        with open(file_path, "wb") as buffer:
            buffer.write(await archivo.read())
        # Devuelve la ruta completa del archivo
        response = {"file_path": file_path}
        # Elimina el archivo después de usarlo
        utils.enviar_imagen("+51922996705", response, msg)
        os.remove(file_path)

        return response


@app.get("/check_navegador/")
async def verificar_navegador():
    utils.check_navegador()
    return "OK"