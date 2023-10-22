from datetime import datetime

import pandas as pd

from Utils import utils

# pywhatkit.sendwhatmsg_to_group_instantly()
# pywhatkit.sendwhats_image()

file = 'Files/contactos.xlsx'

def send_messagge():
    df_contacts = pd.read_excel(file,header=0)
    for index, row in df_contacts.iterrows():
        contact_nro = '+51'+str(row['contacto']).strip()
        mensaje = f"{str(row['pref_msj']).strip()} {str(row['nombre']).strip()} {str(row['suf_msj']).strip()}"
        msg = mensaje
        utils.sendwhatmsg_instantly(contact_nro, msg, tab_close = True, close_time = 1)

send_messagge()
