
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


        // Retornar la respuesta del servidor Flask
        if (response.status === 200) {
            return {
                mensaje: response.data.mensaje,
                imagen_url: response.data.imagen_url || null // Devolver imagen si está presente
            };
        } else {
            throw new Error('Error en la respuesta del servidor Flask');
        }


    } catch (error) {
        console.error(error);
        return { mensaje: 'Hubo un error al procesar tu solicitud.' };
    }
}

module.exports = ProcesarComando;
