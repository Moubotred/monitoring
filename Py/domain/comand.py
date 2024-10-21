from banners import msgBanner

class Commands:  # He corregido el nombre de la clase

    def __init__(self) -> None:
        self.bps = msgBanner()
    @staticmethod
    def cut(comand):
        value = comand.split()
        if len(value) == 1:
            return True
        
        if len(value) == 2:
            if int(value[1]) == int:
                return value[1]
        else:
            return False
            
    def help(self,comand,usuario):
        if self.cut(comand):
            return self.bps.BannerPrincipal(usuario)

    def lg(self,comand,usuario):
        if self.cut(comand):
            return self.bps.SuscripcionExitosa(usuario)
