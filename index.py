from ast import Expression
from xml.dom.minidom import Document, Identified
import pymongo
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


# datos de conexion a la base de datos.
MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIMEOUT = 1000
MONGO_URI  = 'mongodb://'+MONGO_HOST+':'+MONGO_PORT+'/'

MONGO_DB = 'college'
MONGO_COLLECTION = 'students'
cliente = pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS = MONGO_TIMEOUT)
dataBase = cliente[MONGO_DB]
collection = dataBase[MONGO_COLLECTION]
#funcio para conectar python con mongodb 
def showData(): 
    try:
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        for document in collection.find():
            tabla.insert('',0,text=document['_id'],values=document['name'])       
        cliente.close()
    except pymongo.errors.ConnectionFailure as errorConexion:
        print('error conexion to mongodb', errorConexion)
    except pymongo.errors.ServerSelectionTimeoutError as errorTime:
        print('time exceeded'+ errorTime)

def createRecord():
    if len(name.get())!=0 and len(qualification.get())!=0 and len(sex.get())!=0:
        try:
            document = {'name': name.get(), 'sex':sex.get(),'qualification':qualification.get()}
            collection.insert(document)
            name.delete(0,END)
            sex.delete(0,END)
            qualification.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print('error conexion to mongodb', error)
    showData()


#diseñamos la ventana con tkinter 
ventana = Tk()
tabla = ttk.Treeview(ventana,columns=2)
tabla.grid(row=1,column=0,columnspan= 2)

tabla.heading('#0', text='ID')
tabla.heading('#1', text='Name')

#name
Label(ventana,text='name').grid(row=2,column=0)
name = Entry(ventana)
name.grid(row=2,column=1)
#sex
Label(ventana,text='sex').grid(row=3,column=0)
sex = Entry(ventana)
sex.grid(row=3,column=1)
#qualification
Label(ventana,text='qualification').grid(row=4,column=0)
qualification = Entry(ventana)
qualification.grid(row=4,column=1)

create = Button(ventana,text='Create',command=createRecord,bg='green',fg='white')
create.grid(row=5,columnspan=2)


showData()

ventana.mainloop()


