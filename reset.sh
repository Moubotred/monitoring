if ! pgrep -u "$USER" ssh-agent > /dev/null; then
    eval "$(ssh-agent -s)" > /dev/null
fi

# Agregar la clave privada al agente si no está agregada
ssh-add -l > /dev/null 2>&1
if [ $? -ne 0 ]; then
    ssh-add ~/.ssh/id_rsa < /dev/null
fi