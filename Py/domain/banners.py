class msgBanner:
    def activate(self):
        pass
    def deactivate(self):
        pass
    def BannerPrincipal(self,usuario):
        bp = f"""
Hola, {usuario}, bienvenido a la guía básica de Doex.
Si aún no te has registrado, utiliza el comando /rg
Este comando creará un perfil en nuestra base de datos, 
el cual es necesario para utilizar este bot.
        """
        return bp
    def Avisos(self):
        pass
    def SuscripcionExitosa(self,usuario):
        S_C_E = f"""
Hola {usuario} Te has registrado correctamente [✅]
🌟 te uniste al bot bienvenid@!
[⚡️] PLAN: BASICO
[🔒] ROL: USUARIO
[🗓] VENCIMIENTO: NINGUNO
"""
        return S_C_E