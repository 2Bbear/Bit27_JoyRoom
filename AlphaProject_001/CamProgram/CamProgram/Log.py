import inspect
i=0
def L_Flow():
    global i
    i=i+1
    classname=str(inspect.stack()[1][1])
    word=classname.split('\\')
    print(str(i)+"_"+word[-1]+"."+str(inspect.stack()[1][3]))


    
    
