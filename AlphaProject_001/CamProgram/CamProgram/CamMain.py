#Teem Libliry
import CamManager

#Custom Libliry
import Log as l
class CamMain:
    cm=CamManager.CamManger()
    def __init__(self):
        l.L_Flow()
        pass
    def __del__(self):
        l.L_Flow() 
        pass

    #Override

    #Team Method
    def Init(self):
        l.L_Flow() 
        
        pass

    def Run(self):
        l.L_Flow() 
        self.cm.Run()
        pass

    def End(self):
        l.L_Flow() 
        pass
if __name__ == "__main__":
    instance=CamMain()
    instance.Init()
    instance.Run()
    instance.End()
    
