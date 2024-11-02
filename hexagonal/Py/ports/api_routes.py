from flask import Blueprint, request, jsonify
# from domain.services.procesar_comando_suscripcion import ProcesarComandoSuscripcion
from domain.comand import Commands as Cmd

from domain.banners import msgBanner

# from py.adapters.adapter import Luzdelsur_Recibo
# from py.adapters.adapter import Hasber_Sistema_Envios

api_bp = Blueprint('api', __name__)

@api_bp.route('/procesar_comando', methods=['POST'])
def procesar_comando():
    data = request.json
    comando = data.get('comando')
    nameUser = data.get('usuario_id')
    
    cmd_instance = Cmd()
    Msg_banner = msgBanner()

    if comando.startswith('/help'):
        # if cmd_instance.cut(comando):
            # servicio = cmd_instance.help(comando,nameUser)
            Msg_banner.BannerPrincipal(nameUser)
            imagen_url = "https://raw.githubusercontent.com/Moubotred/monitoring/main/ico/image.png"
            return jsonify({'mensaje': Msg_banner, 'imagen_url': imagen_url}), 200

    if comando.startswith('/lg'):
        if cmd_instance.cut(comando):
            servicio = cmd_instance.lg(comando,nameUser)
            return jsonify({'mensaje': servicio}), 200
    
    # if comando.startswith('/u'):
    #     pass

    # if comando.startswith('/p'):
    #     if Cmd.cut():
    #         suministro = Cmd.cut()
    #         await servicio = Hasber_Sistema_Envios()
        
    # if comando.startswith('/r'):
    #     await servicio = Luzdelsur_Recibo()

    # # else:
    return jsonify({'mensaje': 'Comando no reconocido'}), 400
    
    # resultado = servicio.ejecutar(comando, usuario_id)
    # return jsonify(resultado), 200
