
// Adaptadores (Adapters): Implementan los puertos y 
// conectan el núcleo con tecnologías específicas 
// (bases de datos, UI, servicios externos, etc.).

const axios = require('axios');
const { FLASK_URL } = require('../config');

async function ProcesarComando(comando, usuarioId) {
    try {
        const response = await axios.post(`${FLASK_URL}/api/procesar_comando`, {
            comando,
            usuario_id: usuarioId
        });
        return response.data;
    } catch (error) {
        console.error(error);
        return { mensaje: 'Hubo un error al procesar tu solicitud.' };
    }
}

module.exports = ProcesarComando;
