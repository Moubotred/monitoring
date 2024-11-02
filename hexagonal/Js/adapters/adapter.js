// Adaptadores (Adapters): Implementan los puertos y conectan el núcleo con 
// tecnologías específicas (bases de datos, UI, servicios externos, etc.).

const qrcode = require('qrcode-terminal');
const { Client, LocalAuth, MessageMedia, MessageAck } = require('whatsapp-web.js');
// const adapter = require('../services/procesar_comando');
const ProcesarComando = require('../ports/procesar_comando');

class WhatsAppClient {
    constructor() {
        this.client = new Client({
            authStrategy: new LocalAuth(),
            puppeteer: {
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            }
        });
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.client.on('qr', this.onQR.bind(this));
        this.client.on('authenticated', this.onAuthenticated.bind(this));
        this.client.on('auth_failure', this.onAuthFailure.bind(this));
        this.client.on('ready', this.onReady.bind(this));
        this.client.on('message', this.onMessage.bind(this));
    }

    onQR(qr) {
        console.log('QR code received, scan please!');
        qrcode.generate(qr, { small: true });
    }

    onAuthenticated() {
        console.log('Authenticated successfully!');
    }

    onAuthFailure(msg) {
        console.error('Authentication failure:', msg);
    }

    onReady() {
        console.log('Client is ready!');
    }

    async onMessage(message) {
        const contact = await message.getContact();
        const contactName = contact.pushname || contact.notifyName || 'Undefined';
        const comando = message.body;
        const usuarioId = message.from; // Asumiendo que 'from' es el ID del remitente

        if (typeof comando === 'string' && comando.startsWith('/')) {
            try {
                const respuesta = await ProcesarComando(comando,contactName);

                if (respuesta.imagen_url) {
                    const media = await MessageMedia.fromUrl(respuesta.imagen_url);
                    await this.sendMediaMessage(usuarioId, media);
                }
                
                await this.sendMessage(usuarioId, respuesta);
            } catch (error) {
                console.error('Error al procesar el comando:', error);
                await this.sendMessage(usuarioId, 'Lo siento, ocurrió un error al procesar tu comando.');
            }
        }
    }

    async sendMessage(to, message) {
        try {
            const chat = await this.client.getChatById(to);
            const sentMessage = await chat.sendMessage(message);
            console.log('Mensaje enviado:', sentMessage.id._serialized);
            return sentMessage;
        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            throw error;
        }
    }


    initialize() {
        this.client.initialize();
    }
}

module.exports = WhatsAppClient;