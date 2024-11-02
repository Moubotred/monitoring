const WhatsAppClient = require('./adapters/adapter');
const procesarComando = require('./ports/procesar_comando');

const whatsappClient = new WhatsAppClient();
whatsappClient.initialize();