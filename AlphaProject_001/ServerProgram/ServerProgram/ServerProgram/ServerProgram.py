
#Team Libliry
import ServerManager
#Custom Libliry
import Log as l
# -*- coding: utf-8 -*-
class ServerMain:
    sm=None

    def __init__(self):
        l.L_Flow()
        
        pass

    def __del__(self):
        l.L_Flow()
        pass

    def Init(self):
        l.L_Flow()
        self.sm=ServerManager.ServerManager()
        pass

    def Run(self):
        l.L_Flow()
        self.sm.Run()
        pass

    def End(self):
        l.L_Flow()
        pass

if __name__ == "__main__":
    sp=ServerMain()
    sp.Init()
    sp.Run()
    sp.End()
    pass