const fs = require('fs');
const os = require('os');
const { exec } = require('child_process');
const qrcode = require('qrcode-terminal');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');

const utils = require('./utils');

const Chance = require('chance');
const chance = new Chance();
const fileName = chance.string({ length: 7, pool: '1234567' }) + '.jpg';


const username = os.userInfo().username;

const archivoSuscriptores = './suscriptores.json';

// correccion temporal de registro de usuarios 
// error sucede cuando se detiene el script y se inicia 
// nuavemete se debe registra nuevamente para poder usar los comandos
const suscriptores = {};
if (fs.existsSync(archivoSuscriptores)) {
    const data = fs.readFileSync(archivoSuscriptores, 'utf8');
    try {
        suscriptores = JSON.parse(data);
    } catch (error) {
        console.error('Error al parsear suscriptores:', error);
    }
}

// Initialize the client with proper Puppeteer options
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Generate and display the QR code
client.on('qr', qr => {
    console.log('QR code received, scan please!');
    qrcode.generate(qr, { small: true });
});

// Log authentication success
client.on('authenticated', () => {
    console.log('Authenticated successfully!');
});

// Handle authentication failure
client.on('auth_failure', msg => {
    console.error('Authentication failure:', msg);
});

// Client is ready to receive messages
client.on('ready', () => {
    console.log('Client is ready!');
});

client.on('message', async message => {
    const contact = await menssage.getContact();
    utils.logMessageToFile(`By: Message: ${message.body}`);

    if (message.body === '/help'){
        utils.help(message)
    }
    else if (message.body === '/lg') {
        suscriptores[message.from] = true;
        utils.guardarSuscriptores(archivoSuscriptores, suscriptores, message);
    }

    if (suscriptores[message.from] === true){
        // Verificar si el comando /s tiene al menos dos partes y el argumento no está vacío
        const contact = await message.getContact();
        const contactName = contact.pushname || contact.notifyName || 'Undefined';
        const partes = message.body.split(' ');
        const suministro = message.body.split(' ')[1];        

        if (suscriptores[message.from] === true && message.body.startsWith('/i') && message.hasMedia) {
            console.log(`by: ${contactName}`);
            console.log('Command:',message.body);   
            if (message.hasMedia) {
                const media = await message.downloadMedia();
                if (media) {
                    // Guarda la imagen en el disco
                    const fileName = chance.string({ length: 7, pool:'1234567'}) + '.jpg';
                    fs.writeFileSync(`/home/${username}/monitoring/py/tmp/${fileName}`, media.data, 'base64');
    
                    const value = utils.execution_cmd(fileName,'apiImg',message)
                        .then(resultado=>{
                            if (resultado.trim().endsWith('.pdf')) {
                                const pdf = MessageMedia.fromFilePath(`/home/${username}/monitoring/py/pdf/${resultado}`.trim());
                                message.reply(`Respuesta: ${resultado}`, undefined, { media: pdf, quotedMessageId: message.id._serialized });
                                console.log(`ReponsePython: envio existoso ${resultado}`);
                            }
                            // message.reply(`Respuesta: ${resultado}`);
                            // console.log(`ReponsePython: ${resultado}`);
                        })
    
                        .catch(error =>{
                            console.log(`ReponsePython: ${error}`);
                        })
    
                }
            }
        }

        // console.log(suministro);
        // if (partes.length < 2 || partes[1].trim() === '') {
            // utils.argument_management(partes,message)
        // }
        if (!isNaN(suministro) && suministro.length >= 1 && suministro.length <= 7) {

            console.log(`by: ${contactName}`);
            console.log('Command:',message.body);

            if (message.body.startsWith('/s ')) {
            
                const value = utils.execution_cmd(suministro,'apiUrl',message)
                    .then(resultado=>{
                        message.reply(`Respuesta: ${resultado}`);
                        console.log(`ReponsePython: ${resultado}`);
                    })
    
                    .catch(error =>{
                        console.log(`ReponsePython: ${error}`);
                    })
    
            }
    
            if (message.body.startsWith('/d ')) {
    
                const value = utils.execution_cmd(suministro,'apiDoc',message)
                    .then(resultado =>{
                        utils.sendfile(resultado,suministro,message)
                    })
    
                    .catch(error =>{
                        console.log(error);
                    })
            }
            
            // if (message.body.startsWith('/i') && message.hasMedia) {
            //     if (message.hasMedia) {
            //         const media = await message.downloadMedia();
            //         if (media) {
            //             // Guarda la imagen en el disco
            //             fs.writeFileSync('/home/kimshizi/Documents/test/py/tmp/over.jpg', media.data, 'base64');
            //             console.log('Imagen descargada');
            //         }
            //     }
            // }
                    
        }

    }

});


client.initialize();
