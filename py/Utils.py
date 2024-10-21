import argparse
import ResourceHub as Rb  # Asumiendo que Rb es un módulo que has importado 
import Apis

ip = '127.0.0.1'
port = '5000'
key_data = 'result'
# http://localhost:5000/process_supply

def apiUrl(sum_value):
    endpoint = 'process_supply'
    rs = Rb.ConsultApi(ip, port, endpoint, key_data, sum_value)    
    print(rs)

def apiDoc(sum_value):
    endpoint = 'process_convert_pdf'
    # mensaje = Rb.Hasber_Sistema_Envios(sum_value)
    raw_url = Rb.ConsultApi(ip, port, endpoint, key_data, sum_value)    
    print(raw_url)
    
def apiImg(sum_value):
    """
    Función de reserva para procesar imágenes. Actualmente no implementada.

    Parameters:
    sum_value (str): El valor de entrada para procesar la imagen.
    
    Returns:
    None: Esta función aún no tiene implementación.
    """
    endpoint = 'process_image_a_pdf'
    raw_url = Rb.ConsultApi(ip, port, endpoint, key_data, sum_value)    
    print(raw_url)
    
def apiRec(sum_value):
    """
    Función de consulta recibo de su suministro buscando en la web de lds.

    Parameters:
    sum_value (str): El valor de entrada del suministro
    
    Returns:
    None: Esta función aún no tiene implementación.
    """
    
    raw_url = Rb.ConsultaApiLds(sum_value)    
    print(raw_url)

def main():
    """
    Función principal que utiliza argparse para parsear los argumentos de la línea de comandos.
    Según el modo seleccionado ('apiUrl' o 'apiDoc'), llama a las funciones respectivas para consultar 
    la API o procesar documentos.

    Parameters:
    None: No toma parámetros directos, pero procesa los argumentos de la línea de comandos.
    
    Returns:
    None: Ejecuta la función correspondiente según el modo de operación.
    """
    parser = argparse.ArgumentParser(description="Herramienta de utilidad para procesar datos.")
    
    parser.add_argument('sum', type=str, help='Valor de suma o identificador.')
    parser.add_argument('--mode', type=str, choices=['apiUrl', 'apiDoc','apiImg','apiRec'], required=True,
                        help="Modo de operación: 'apiUrl' para consultar la API o verificar caché, 'apiDoc' para descargar y convertir.")

    args = parser.parse_args()

    if args.mode == 'apiUrl':
        apiUrl(args.sum)
    elif args.mode == 'apiDoc':
        apiDoc(args.sum)
    elif args.mode == 'apiImg':
        apiImg(args.sum)
    elif args.mode == 'apiRec':
        apiRec(args.sum)

if __name__ == '__main__':
    main()
