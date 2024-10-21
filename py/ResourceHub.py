import os
import json
import time
import shutil
import urllib.parse
import re

from Constant import exp

import urllib.request
from getpass import getuser
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException
import aspose.words as aw

import os
import time
import platform
import subprocess

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from BetaApiLds import api
import shutil

request_logs = []
DD = 'tmp'

def cache(suministro):
    path = f'/home/{getuser()}/Documents/test/py/pdf'
    os.makedirs(path, exist_ok=True)
    
    pdf_filename = f"{suministro}.pdf"
    if pdf_filename in os.listdir(path):
        return os.path.join(path, pdf_filename)
    else:
        return None

def SearchFileWeb(suministro):
    global wait
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 60)
    driver.get('https://hasbercourier.easyenvios.com/')

    sandbox = wait.until(EC.presence_of_element_located((By.ID, exp.box)))
    sandbox.send_keys(suministro)

    sendContent = wait.until(EC.presence_of_all_elements_located((By.XPATH, exp.btn)))
    sendContent[0].click()

    time.sleep(2)

    table_send = wait.until(EC.presence_of_all_elements_located((By.XPATH, exp.table)))
    for n_ in range(len(table_send)):
        table_tr = wait.until(EC.presence_of_element_located((By.XPATH,exp.tr.replace('@',f'{n_+1}')))).click()
        info = wait.until(EC.presence_of_element_located((By.ID,'sp_cargo_documento'))).text
        if 'CARTAS / REEMPLAZO DE MEDIDOR EMPRESAS' == info:
            time.sleep(2)
            Framesubdoc = wait.until(EC.presence_of_element_located((By.ID, exp.subdoc))).get_attribute('src')
            driver.quit()
            print(Framesubdoc)
            return Framesubdoc, suministro
        else:
            pass

def UrlSubdoc(Framesubdoc):
    ParsedUrl = urlparse(Framesubdoc)
    QueryParams = parse_qs(ParsedUrl.query)
    Url = QueryParams.get('url', [None])[0]
    return Url

def FileWebDownloads(url, suministro):
    try:
        if url != 'http://www.easyenvios.com/escan1/006/003/3/00000001/01/00300000001000001.TIF':
            filename = suministro + '.tif'
            with urllib.request.urlopen(urllib.request.Request(url)) as response, open(filename, "wb") as out_file:
                data = response.read()
                out_file.write(data)
                out_file.close()
            return filename
        else:
            return None
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return None

def ConvertPdf(filename):
    #os.environ['DOTNET_SYSTEM_GLOBALIZATION_INVARIANT'] = '1'
    if filename:
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)
        builder.insert_image(filename)
        pdf_filename = filename.replace('.tif', '.pdf')
        doc.save(pdf_filename)
        return pdf_filename
    else:
        return False

def Templades(pdf_filename):
    if pdf_filename:
        path = f'/home/{getuser()}/Documents/monitoring/py/pdf'
        os.makedirs(path, exist_ok=True)

        shutil.move(pdf_filename, os.path.join(path, pdf_filename))
        os.remove(pdf_filename.replace('.pdf', '.tif'))
    else:
        print("No se encontró el archivo PDF para aplicar la plantilla.")

def ConsultApi(ip, port, endpoint, key_data, suministro):
    
    # Si no se encuentra en la caché, procede con la solicitud
    url = f"http://{ip}:{port}/{endpoint}"

    data = {
        "suministro": suministro
    }

    data_bytes = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            result = json.loads(response_data)
            data_r = result.get(key_data)
            # Registrar la solicitud y la respuesta
            # log_request(suministro,data_r,filename='request_logs.json')
            if data_r is None:
                return 
            return data_r
        
    except urllib.error.HTTPError as e:
        print(f'Error HTTP: {e.code} - {e.reason}')
    except urllib.error.URLError as e:
        print(f'Error URL: {e.reason}')
    
    return None

def ConsultaApiLds(suministro):
    home_dir = os.path.expanduser('~')
    imagenes = os.path.join(home_dir,'monitoring','BetaApiLds','imagenes')
    if os.path.exists(imagenes) == True: 
        numero_S = api.Recibo(suministro)
        shutil.move(os.path.join(os.getcwd(),numero_S),os.path.join(imagenes,numero_S))
        return numero_S
    else:
        os.makedirs(imagenes)
        ConsultaApiLds(suministro)

import requests
import urllib.request

def Hasber_Sistema_Envios(suministro):
    # URL a la que se va a hacer la solicitud POST
    url = "https://hasbercourier.easyenvios.com/modulos/controlador/herramientas/con_cargosenvios.php?tabla=congrid_envio_seguimiento"

    # Encabezados
    headers = {
        "Host": "hasbercourier.easyenvios.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://hasbercourier.easyenvios.com",
        "Referer": "https://hasbercourier.easyenvios.com/modulos/seguimiento.php",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
        "Connection": "keep-alive"
    }

    # Parámetros del cuerpo de la solicitud (POST data)
    data = {
        "ciacodigo": "17",
        "succodigo": "001",
        "asenombre": "",
        "codigoenvio": "",
        "codigounico": f"{suministro}",
        "asepropuesta": "",
        "strnrodocumento": "",
        "page": "1",
        "rows": "10",
        "sort": "a.asenumero",
        "order": "asc"
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, data=data)

    # Verificar el estado de la respuesta de estado
    if response.status_code == 200:
        # pasar datos a json
        data = response.json()
        try:
            # buscar clave de diccionario
            filename = f'{suministro}.tif'
            values_boolean = [data['rows'][i]['artnombre'] == 'CARTAS / REEMPLAZO DE MEDIDOR EMPRESAS' for i in range(len(data['rows']))]
            if values_boolean:
                url_file = data['rows'][values_boolean.index(True)]['imagen1']
                FileWebDownloads(url_file,suministro)
                filename = ConvertPdf(filename)
                Templades(filename)
            else:
                return False

        except IndexError:
            return False
    else:
        return False

def Directorios(directorio):
    def Servidor(func):
        def python(*args,**kwargs):
            if directorio:
                target_dir = os.path.join(os.getcwd(),directorio)  # Subdirectorio

            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            os.chdir(target_dir)
            return func(*args, **kwargs)  # Ejecutar la función original
        return python
    return Servidor

from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            end = time.time()
            print(f"Error in {func.__name__}: {e}")
            print(f"[!] Funcion: {func.__name__} tiempo de respuesta: {end - start:.2f} segundos")
            raise
        end = time.time()
        print(f"\n[+] Funcion: {func.__name__} tiempo de respuesta: {end - start:.2f} segundos")
        return result
    return wrapper

from multiprocessing.pool import ThreadPool
import threading


urlTunnel = None

# -------- importaciones necesarias sino causa errores al momento de combinarlo con flask cuando se llama a Servicios
from multiprocessing.synchronize import Lock
from multiprocessing.queues import SimpleQueue
from multiprocessing.dummy import Process
# -------------------------------------------------------------------------------------------------------------------

import requests
from deprecated import deprecated
from pyngrok import conf,ngrok
from pyngrok.exception import PyngrokNgrokError

@Directorios(DD)
def ServicioPython():
    so = platform.system() 
    python = 'python3' if so == 'Linux' else 'python'
    subprocess.Popen([f"{python}", "-m", "http.server", "5090"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('[+] Corriendo Servidor Python')

def Apilocalngrok():
    try:
        # Realizar una petición GET a la API local de ngrok
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        response.raise_for_status()  # Verificar si hubo errores en la petición
        
        # Parsear la respuesta JSON
        tunnels_info = response.json()
        tunnels = tunnels_info.get('tunnels', [])
        
        if tunnels:
            for tunnel in tunnels:
                return tunnel.get('public_url')
        else:
            print("[!] No hay túneles activos")
    except requests.exceptions.ConnectionError:
        print("[!] Asegúrate de que ngrok esté en ejecución manualmnete")
    except Exception as e:
        print(f"[!] Error al obtener los túneles: {str(e)}")
    
def Servicios():
    global urlTunnel

    # Crear hilos
    t1 = threading.Thread(target=ServicioPython)

    # Iniciar los hilos
    t1.start()

    # Dar tiempo para que ngrok inicie
    time.sleep(2)

    # Esperar que ambos hilos terminen (opcional dependiendo de si quieres continuar después)
    t1.join()
    # t2.join()

def GoogleLents(driver,wait,tunnel,filename):

    waits = WebDriverWait(driver, 10)

    list_information = []

    driver.execute_script("window.open('https://www.google.com/search?client=firefox-b-d&q=ll', '');")
    driver.switch_to.window(driver.window_handles[-1])

    driver.refresh()

    lents = waits.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nDcEnd'))).click()

    enlace = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cB9M7[jsname="W7hAGe"]')))

    enlace = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cB9M7[jsname="W7hAGe"]')))

    # enlace = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cB9M7[jsname="W7hAGe"]')))

    enlace.click()
    enlace.send_keys(tunnel+'/'+filename)

    search = wait.until(EC.element_to_be_clickable((By.XPATH,exp.search))).click()
    translate = wait.until(EC.element_to_be_clickable((By.ID, 'ucj-3'))).click()

    # Localizar el contenedor principal
    container = wait.until(EC.presence_of_element_located((By.CLASS_NAME,exp.contenedor)))

    # Localizar todos los 'div' hijos dentro del contenedor
    child_divs = container.find_elements(By.XPATH,exp.elementos)

    # Obtener el texto de cada uno de los elementos
    for div in child_divs:
        result = re.sub(r'\D', '', div.text)
        if result:
            list_information.append(result)
            
    driver.close()
    driver.switch_to.window(driver.window_handles[0])    
    
    return list_information[0] 
