
# Adaptadores (Adapters): Implementan los puertos y 
# conectan el núcleo con tecnologías específicas 
# (bases de datos, UI, servicios externos, etc.).

import asyncio
import aiohttp
import base64
import utis.tools

async def Luzdelsur_Recibo(suministro):
    # URL de la API
    url = "https://www.luzdelsur.pe/es/VerPagarRecibo/ObtenerImagenBoletaLibre"

    # Payload con el número de suministro
    payload = {
        "request": {
            "Suministro": f"{suministro}"
        }
    }

    # Encabezados necesarios
    headers = {
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

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("success"):
                    imagen_base64 = data['datos']['archivoBase64']
                    with open(f"{suministro}.png", "wb") as img_file:
                        try:
                            img_file.write(base64.b64decode(imagen_base64))
                            return suministro
                        except TypeError:
                            return "[x] La API no devolvió una imagen válida"
                
            else:
                return f"[x] Error en la solicitud: {response.status}"

async def Hasber_Sistema_Envios(suministro):
    
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
    payload = {
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
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            # Verificar el estado de la respuesta de estado
            if await response.status_code == 200:
                # pasar datos a json
                data = response.json()
                try:
                    # buscar clave de diccionario
                    if data['rows'][0]['artnombre'] == 'CARTAS / REEMPLAZO DE MEDIDOR EMPRESAS':
                        url_file = data['rows'][0]['imagen1']
                        namefile = f'{suministro}.tif'
                        utis.tools.Download(url_file,suministro)       
                        utis.tools.Convert(namefile)
                        utis.tools.Remove(namefile)
                        return suministro                    
                except IndexError:
                    return '?'
            else:
                print('[x]')
