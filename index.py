import pymongo
from tkinter import *
from tkinter import ttk
from tkinter import messagebox



MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIMEOUT = 1000
MONGO_URI  = 'mongodb://'+MONGO_HOST+':'+MONGO_PORT+'/'

MONGO_DB = 'college'
MONGO_COLLECTION = 'students'

def showData(tabla): 
    try:
        cliente = pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS = MONGO_TIMEOUT)
        dataBase = cliente[MONGO_DB]
        collection = dataBase[MONGO_COLLECTION]

        for document in collection.find():
            tabla.insert('',0,text=document['_id'],values=document['name'])


        #print('successful connection')
        #cliente.close()
    except pymongo.errors.ConnectionFailure as errorConexion:
        print('error conexion to mongodb'+ errorConexion)
    except pymongo.errors.ServerSelectionTimeoutError as errorTime:
        print('time exceeded'+ errorTime)


if __name__=='__main__':
    ventana = Tk()
    tabla = ttk.Treeview(ventana, columns = 2)
    tabla.grid(row=1,column=0,columnspan=2)
    tabla.heading('#0', text='ID')
    tabla.heading('#1', text='Name')
    showData(tabla)

    ventana.mainloop()


