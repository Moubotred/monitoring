const WhatsAppClient = require('./adapters/adapter');
const procesarComando = require('./ports/procesar_comando');

const whatsappClient = new WhatsAppClient();

// Modificar el método onMessage en la clase WhatsAppClient
whatsappClient.onMessage = async (message) => {
    const comando = message.body;
    const usuarioId = message.from; // Asumiendo que 'from' es el ID del remitente
    const respuesta = await procesarComando(comando, usuarioId);
    await whatsappClient.sendMessage(usuarioId, respuesta.mensaje);
};

whatsappClient.initialize();