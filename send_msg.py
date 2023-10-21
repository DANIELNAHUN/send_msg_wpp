from datetime import datetime
from Utils import utils
import pandas as pd

# pywhatkit.sendwhatmsg_instantly("+51922996705", "Hola")
# pywhatkit.sendwhatmsg_to_group_instantly()
# pywhatkit.sendwhats_image()


contact_nro = ''
msg = ''

file = 'Files/contactos.xlsx'




def send_messagge():
    df_contacts = pd.read_excel(file)
    print(df_contacts)
    for contact in df_contacts:
        contact_nro = str(contact['contacto'])
        print(contact_nro)
    # utils.sendwhatmsg_instantly("+51922996705", f"Hola", tab_close = True, close_time = 1)

send_messagge()
