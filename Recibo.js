const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

// Inicializa el cliente de WhatsApp
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});


client.on('qr', qr => {
    // Genera el código QR para la autenticación
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('El cliente está listo.');

    // Especifica el número de teléfono al que deseas enviar la imagen
    const chatId = '51915985153@c.us'; // Reemplaza con el número de teléfono en formato internacional (con el código de país)

    // Ruta de la imagen que deseas enviar
    const imagePath = `${__dirname}/BetaApiLds/imagenes/143355.png`;

    // Lee el archivo PNG como un buffer
    const media = MessageMedia.fromFilePath(imagePath);

    // Envía la imagen al chat
    client.sendMessage(chatId, media)
        .then(response => {
            if (response.id.fromMe) {
                console.log('Imagen enviada exitosamente.');
            }
        })
        .catch(error => {
            console.error('Error al enviar la imagen:', error);
        });
});

client.on('message', message => {
    console.log(`Mensaje recibido: ${message.body}`);
});

// Inicia sesión en el cliente
client.initialize();
