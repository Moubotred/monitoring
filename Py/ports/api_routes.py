from flask import Blueprint, request, jsonify
# from domain.services.procesar_comando_suscripcion import ProcesarComandoSuscripcion
from domain.comand import Commands as Cmd
from py.adapters.adapter import Luzdelsur_Recibo
from py.adapters.adapter import Hasber_Sistema_Envios

api_bp = Blueprint('api', __name__)

@api_bp.route('/procesar_comando', methods=['POST'])
async def procesar_comando():
    data = request.json
    comando = data.get('comando')
    usuario_id = data.get('usuario_id')
    
    if comando.startswith('/help'):
        if Cmd.cut(comando):
            servicio = Cmd.help()

    if comando.startswith('/lg'):
        if Cmd.cut(comando):
            servicio = Cmd.lg()
    
    if comando.startswith('/u'):
        pass

    if comando.startswith('/p'):
        if Cmd.cut():
            suministro = Cmd.cut()
            await servicio = Hasber_Sistema_Envios()
        
    if comando.startswith('/r'):
        await servicio = Luzdelsur_Recibo()

    # else:
    #     return jsonify({'mensaje': 'Comando no reconocido'}), 400
    
    resultado = servicio.ejecutar(comando, usuario_id)
    return jsonify(resultado), 200
