const {exec} = require('child_process');
const fs = require('fs');
const {MessageMedia } = require('whatsapp-web.js');
const axios = require('axios');
const path = require('path');
const os = require('os');


const username = os.userInfo().username;

async function localendpoint(endpoint, suministro) {
    const url = `http://127.0.0.1:8000/${endpoint}`;
    const start = performance.now();
  
    try {
      const response = await axios.get(url, { params: { suministro: suministro } });
      const end = performance.now();
      const elapsed = (end - start) / 1000; // Ahora en segundos
      return {
        suministro: response.data.suministro,
        elapsed
      };
    } catch (error) {
      const end = performance.now();
      const elapsed = (end - start) / 1000; // Ahora en segundos
    //   let detail = "Error desconocido";
  
      if (error.response && error.response.data && error.response.data.detail) {
        detail = error.response.data.detail;
      } else if (error.response && error.response.data) {
        detail = JSON.stringify(error.response.data);
      }
  
      return { detail, elapsed };
    }
  }
  
  function chunckis(respuesta, message) {
    try {
    const suministro = respuesta.suministro;
    const elapsed = respuesta.elapsed;

    if (suministro.endsWith('.pdf')) {
        const pdfPath = `${__dirname}/descargas/pdf/${suministro}`;
        const pdf = MessageMedia.fromFilePath(pdfPath);
        message.reply(`✅ status: exito \n📌 mensaje: ${suministro}\n⏰ Tiempo: ${elapsed.toFixed(2)} s`, undefined, { media: pdf, quotedMessageId: message.id._serialized });
        console.log(`ReponsePython: envío exitoso ${suministro}`);

    } else if (suministro.endsWith('.png')) {
        const imagePath = `${__dirname}/descargas/png/${suministro}`;
        const image = MessageMedia.fromFilePath(imagePath);
        message.reply(`✅ status: exito \n📌 mensaje: ${suministro}\n⏰ Tiempo: ${elapsed.toFixed(2)} s`, undefined, { media: image, quotedMessageId: message.id._serialized });
        console.log(`ReponsePython: envío exitoso ${suministro}`);
    }
  
    } catch {
        const detail = respuesta.detail;
        const elapsed = respuesta.elapsed;
        message.reply(`❌ status: fallo \n${detail}\n⏰ Tiempo: ${elapsed.toFixed(2)} s`);
    }
  }


function help(message) {
    // const banner = '🤖 Bienvenido al bot:\n\ncomandos:\n\n/lg suscribir al bot\n/s obtener url\n/d obtener pdf';
    const banner = `👑 Fundador:
        └ @L.T.A 
    ⚜ Descripcion:
    ├   La Herramienta ayuda
    ├   con la gestion de  
    └   consultas de hasber   

    ⚜ Comandos:
    ├
    ├ /lg regitrar usuario 
    ├ /s solicitar url de carta
    ├ /d solicitar pdf de carta
    └ /i solicitar carta por foto
        └ ⚜ Ejemplo de uso :
            ├ /s 1337535
            └ /d 1337535
            └ /i [file]
    ⚜ Reportes o mejoras: 
    ├
    ├ ayudame a mejor el bot 
    ├ o agregar nuevas funciones
    └ escribeme al numero 915985153
    `;

    message.reply(banner);
}

// Función para guardar suscriptores en un archivo JSON
function guardarSuscriptores(filesuscription, suscriptores, message) {
    fs.writeFileSync(filesuscription, JSON.stringify(suscriptores, null, 2));
    message.reply('Usuario registrado');
}

// Función para cargar suscriptores desde un archivo JSON
function database(filesuscription) {
    let suscriptores = {};
    if (fs.existsSync(filesuscription)) {
        suscriptores = JSON.parse(fs.readFileSync(filesuscription, 'utf-8'));
    }
    return suscriptores;
}

function argument_management(partes,message){
    message.reply(`Respuesta: command ${partes[0]} requiere suministro`);
    console.error(`ReponsePython: command ${partes[0]} requiere suministro`);
    return;
}

function sendfile(evalue,numero,message){
    if (evalue.trim().endsWith('.pdf')) {
        const pdf = MessageMedia.fromFilePath(`${__dirname}/descargas/pdf/${numero}.pdf`);
        message.reply(`Respuesta: ${evalue}`, undefined, { media: pdf, quotedMessageId: message.id._serialized });
        console.log(`ReponsePython: envio existoso ${evalue}`);

    } else if (evalue.trim().endsWith('.png')) {
        const imagePath = `${__dirname}/descargas/png/${numero}.${evalue.trim().split('.').pop()}`;
        const image = MessageMedia.fromFilePath(imagePath);
        message.reply(`Respuesta: ${evalue}`, undefined, { media: image, quotedMessageId: message.id._serialized });
        console.log(`ReponsePython: envío exitoso ${evalue}`);

    } else if (evalue.trim() === "[ ❌] Suminstro no programado para cambio de maximetro") {
        message.reply(`${evalue}`)
        console.log(`Respuesta:${evalue}`)
        }
    
    }

function execution_cmd(suministro, mode, message) {
    // Validación básica de parámetros
    if (typeof suministro !== 'string' || typeof mode !== 'string') {
        throw new Error('Los parámetros suministro y mode deben ser cadenas');
    }
    return new Promise((resolve, reject) => {
        exec(`python3 ~/Proyects/monitoring/py/Utils.py ${suministro} --mode ${mode}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error ejecutando el script: ${error.message}`);
                reject(error);
                return;
            }
            if (stderr) {
                console.error(`Error estándar: ${stderr}`);
                reject(stderr);
                return;
            }
            resolve(stdout);
        });
    });
}

function logMessage(message, type = 'info') {
    const timestamp = new Date().toISOString();
    
    switch (type) {
        case 'info':
            console.log(`[INFO] ${timestamp}: ${message}`);
            break;
        case 'warn':
            console.warn(`[WARN] ${timestamp}: ${message}`);
            break;
        case 'error':
            console.error(`[ERROR] ${timestamp}: ${message}`);
            break;
        default:
            console.log(`[INFO] ${timestamp}: ${message}`);
    }
}

function logMessageToFile(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const logMessage = `[${type.toUpperCase()}] ${timestamp}: ${message}\n`;
    
    // Define la ruta del archivo donde guardar los mensajes de log
    const logFilePath = path.join(__dirname, 'logs.txt');
    
    // Escribe (o añade) el mensaje al archivo
    fs.appendFile(logFilePath, logMessage, (err) => {
        if (err) {
            console.error(`[ERROR] ${timestamp}: No se pudo escribir el log.`);
        }
    });
}

module.exports = {
    help,
    guardarSuscriptores,
    database,
    argument_management,
    execution_cmd,
    sendfile,
    logMessageToFile,
    localendpoint,
    chunckis
};
