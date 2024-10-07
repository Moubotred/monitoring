
![Logo](https://raw.githubusercontent.com/Moubotred/monitoring/main/ico/image(1).png)

# Monitoring

El proyecto ayuda con la gestion del sistema de envios de la web hasber conbinando un bot simple escrito en js que monitorea el chats y cuando se se le hacen consultas con un comando y responde deacuerdor al comando

## Endpoint Referencias

#### POST Rutas

```http
POST api/process_supply
POST api/process_convert_pdf
POST api/process_image_a_pdf
```


## consulta de endpoint

Si quieres usar el endpoint comunicate con fakesarnamer@gmail.com


## Ejecutar en vps



Creacion de usuario
```bash
useradd -m -s /bin/bash $puppeteeruser
passwd 'constrasena'
usermod -aG sudo $puppeteeruser
puppeteeruser ALL=(ALL:ALL) ALL

```
Dependecias

```bash
  sudo apt install -y wget/ python3-venv/   
  python3-pip/ 
  tmux/ git/ curl/ libicu-dev/
  chromium-browser/ libnss3/ libatk1.0-0/
  libatk-bridge2.0-0/ libcups2/ libxcomposite1/   
  libxdamage1/ libxrandr2/ libgbm1/ libasound2/ 
  libpangocairo-1.0-0/ libpango-1.0-0/ libgtk-3-0/ 
 libx11-xcb1/ libxshmfence1/

```

Instalacionde de nodejs

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs npm -y
```

Dependecias de aspose-words en linux 

```bash
  wget https://www.openssl.org/source/openssl-1.1. 
  1c.tar.gz
  tar -xzvf openssl-1.1.1c.tar.gz
  cd openssl-1.1.1c=
  ./config
  make
  sudo make install 
  sudo ln -s /home/puppeteeruser/openssl-1.1.1c/libcrypto.so.1.1 /usr/local/lib/libcrypto.so
```
Enlace simbolico para la libreria de su dependencia de aspose-words

```bash
sudo ln -s /home/puppeteeruser/openssl-1.1.1c/libcrypto.so.1.1 /usr/local/lib/libcrypto.so
```

Configurando .bashrc con nano 
```bash
export LD_LIBRARY_PATH=/home/puppeteeruser/openssl-1.1.1c
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
source .bashrc
```
uso de tmux

```bash
ctrl+b +% | (2)(divide en 3 paneles)
ctrl+b -> (mover hacia el panel derecha)
ctrl+b <- (mover hacia el panel izquierda)
```

Panel 1 tmux

```bash
cd monitoring
tmux new -s nombre de la session
python3 -m venv py/
source py/bin/activate
cd py/
pip install -r req.txt
python3 test_optimizacion
```

Panel 2 tmux

```bash
npm install qrcode-terminal whatsapp-web.js chance
node index.js
```

Panel 3 tmux
```bash
sudo tar xvzf ~/ngrok-v3-stable-linux-arm64.tgz -C /usr/local/bin
ngrok config add-authtoken <token>
ngrok http 5090
```

Mantener en Ejecucion scripts en tmux
```bash
ctrl+b +d
```

Recuperar session de tmux donde corren tus scripts
```bash
tmux -ls
tmux a -t [nombre de la session]
```

## Pruebas

- buscar el chat del bot

- registrase /lg


## Tecnologias Usadas

**Endpoint:** python, flask, selenium

**Bot:** Node, whatsapp-web.js, chance


## Corriendo pruebas

Comando /help brinda ayuda con los comandos
```bash
    `👑 Fundador:
        └ @Lagarto 
        ⚜ Descripcion:
            ├
            ├ bot creado para 
            ├ realizar consultas
            └ al sitio hasber

        ⚜ Comandos:
        ├
        ├ /lg regitrar usuario 
        ├ /s solicitar url de carta
        ├ /d solicitar pdf de carta
        └ /t solicitar carta por foto
            └ ⚜ Ejemplo de uso :
            ├ /s 1337535
            └ /d 1337535   
            
        ⚜ Reportes o mejoras: 
        ├
        ├ ayudame a mejor el bot 
        ├ o agregar nuevas funciones
        └ escribeme al numero 915985153
```
Comando /lg este comando te registra como usuario para poder usar el bot
```bash
/lg 
```


Comando /s este comando envia la url del la carta
```bash
/s 7998
```

Comando /D este comando envia pdf de la carta
```bash
/s 7998
```

Comando /i es neserio adjuntar la foto del suministro el cual reconoce los numero y busca la carta y devuele en pdf
```bash
/i [file]
```
![App Screenshot](https://raw.githubusercontent.com/Moubotred/monitoring/main/ico/file.jpg)
