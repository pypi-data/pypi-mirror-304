import json
import requests
import re
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
import time
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')
WHATSAPP_URL = os.getenv("WHATSAPP_URL")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")

def replace_start(s):
    # Eliminar cualquier carácter que no sea un número
    s = re.sub(r'\D', '', s)

    # Procesar el número
    if s.startswith("549"):
        if s[3:5] == "11":
            # Si comienza con "54911", eliminar el "9" y agregar el "15" después del "11"
            return "54" + s[3:5] + "15" + s[5:]
        elif len(s[3:]) > 9:
            # Si después del "549" hay un código de área de 4 dígitos (como 2233)
            return "54" + s[3:6] + "15" + s[6:]
        else:
            # Para otros casos, eliminar el "9" y agregar el "15"
            return "54" + s[3:5] + "15" + s[5:]
    elif s.startswith("521"):
        if s[3:5] == "11":
            # Si comienza con "52111", eliminar el "1" y agregar el "15" después del "11"
            return "52" + s[3:5] + "15" + s[5:]
        elif len(s[3:]) > 9:
            # Si después del "521" hay un código de área de 4 dígitos (como 2233)
            return "52" + s[3:6] + "15" + s[6:]
        else:
            # Para otros casos, eliminar el "1" y agregar el "15"
            return "52" + s[3:5] + "15" + s[5:]
    else:
        # Si no tiene los prefijos esperados, devolver el número sin cambios
        return s

def upload_media(excel_data):
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}'
    }
    files = {
        'file': (excel_data, open(excel_data, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    }
    data = {
        'type':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'messaging_product': "whatsapp",
    }

    response = requests.post(f"{WHATSAPP_URL}/media", headers=headers, data=data, files=files)
    print(response.json()['id'])
    response.raise_for_status()
    return response.json()['id']
    if response.status_code == 200:
        print(response)
        return response.json().get('id')
    return None

def post_message(data):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {WHATSAPP_TOKEN}'
        }
        response = requests.post(f'{WHATSAPP_URL}/messages', headers=headers, data=data)
        response.raise_for_status()
        return 'Mensaje enviado con éxito', 200
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error al enviar el mensaje: {http_err}")
        return 'Error HTTP al enviar mensaje', response.status_code if 'response' in locals() else 500
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de conexión: {conn_err}")
        return 'Error de conexión al enviar mensaje', 503
    except requests.exceptions.Timeout as timeout_err:
        print(f"Error de tiempo de espera: {timeout_err}")
        return 'El tiempo de espera se agotó al enviar mensaje', 504
    except requests.exceptions.RequestException as req_err:
        print(f"Error inesperado: {req_err}")
        return 'Error inesperado al enviar mensaje', 500
    except Exception as e:
        print(f"Error general: {e}")
        return 'Error general al enviar mensaje', 500


def send_message(number, text):
    try:
        number = replace_start(number)
        data = json.dumps({
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': number,
            'type': 'text',
            'text': {'body': text}
        })
        return data

    except (TypeError, ValueError, json.JSONDecodeError) as e:
        print(f"Error al crear el mensaje JSON: {e}")
        return None

def send_document(number, media_id, filename):
    number = replace_start(number)
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "document",
        "document": {
            "id": media_id,
            "filename": filename
        }
    })
    print(data)
    return data

def manage_chatbot(number, text_to_user):
    try:
        response_text = text_to_user
        data = send_message(number, response_text)
        if data:
            response, status_code = post_message(data)
            return response, status_code
        else:
            print("Error al generar el mensaje")
            return "Error al generar el mensaje", 500
    except Exception as e:
        print(f"Error in manage_chatbot: {e}")
        return f"Error: {str(e)}", 500

def get_media_url(media_id):
    try:
        url = f"https://graph.facebook.com/v20.0/{media_id}/"
        headers = {'Authorization': f'Bearer {WHATSAPP_TOKEN}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('url')
    except requests.exceptions.RequestException as e:
        print(f"Error obteniendo la URL de la media: {e}")
        return None


def download_image(url, max_retries=3, retry_delay=5):

    headers = {'Authorization': f'Bearer {WHATSAPP_TOKEN}'}
    attempt = 0

    while attempt < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.content
        except HTTPError as http_err:
            print(f"Error HTTP al descargar la imagen: {http_err}")
        except ConnectionError as conn_err:
            print(f"Error de conexión al descargar la imagen: {conn_err}")
        except Timeout as timeout_err:
            print(f"Tiempo de espera agotado al descargar la imagen: {timeout_err}")
        except RequestException as req_err:
            print(f"Error al descargar la imagen: {req_err}")

        attempt += 1
        print(f"Reintentando... (Intento {attempt}/{max_retries})")
        time.sleep(retry_delay)

    print("Fallo en la descarga después de varios intentos.")
    return None

def verify_token_service(request):
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if token == TOKEN and challenge:
        return challenge, 200
    else:
        return 'Invalid token', 403
