from ast import Expression
from multiprocessing.connection import Connection
from xml.dom.minidom import Document, Identified
import pymongo
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from bson.objectid import ObjectId


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
ID_STUDENT = ''
#funcio para conectar python con mongodb 
def showData(name='',sex='',qualification=''):
    findObject = {}
    if len(name)!=0:
        findObject['name']= name
    if len(sex)!=0:
        findObject['name']= sex
    if len(qualification)!=0:
            findObject['name']= qualification 
    try:
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
            

        for document in collection.find(findObject):
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
    
    else:
        messagebox.showerror(message='Campos de informacion vacios.')
    showData()


def dobleClipTabla(event):
    global ID_STUDENT
    ID_STUDENT = str(tabla.item(tabla.selection())['text']) 
    document = collection.find({'_id':ObjectId(ID_STUDENT)})[0]
    name.delete(0,END)
    name.insert(0,document['name'])
    sex.delete(0,END)
    sex.insert(0,document['sex'])
    qualification.delete(0,END)
    qualification.insert(0,document['qualification'])
    create['state']='disabled'
    edit['state']='normal'
    deleteD['state']='normal'


def editarRegistro():
    if len(name.get())!=0 and len(sex.get())!=0 and len(qualification.get())!=0:
        try:
            idBuscar = {'_id': ObjectId(ID_STUDENT)}
            nuevosValores={'name':name.get(),'sex':sex.get(),'qualification':qualification.get()}
            collection.update(idBuscar,nuevosValores)
            name.delete(0,END)
            sex.delete(0,END)
            qualification.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print('error conexion to mongodb', error)
    else:
        messagebox.showerror(message='Campos de informacion vacios.')
    create['state']='disabled'
    edit['state']='normal'
    deleteD['state']='disabled'
    showData()


def deleteRecord():
    try:
        idBuscar = {'_id': ObjectId(ID_STUDENT)}
        collection.delete_one(idBuscar)
        name.delete(0,END)
        sex.delete(0,END)
        qualification.delete(0,END)
    except pymongo.errors.ConnectionFailure as error:
        print('error conexion to mongodb', error)
    
    create['state']='normal'
    edit['state']='disabled'
    deleteD['state']='disabled'
    showData()

def findRecord():
    showData(findname.get(), findsex.get(), findqualification.get())
if __name__=='__main__':
#diseñamos la ventana con tkinter 
    ventana = Tk()
    tabla = ttk.Treeview(ventana,columns=2)
    tabla.grid(row=1,column=0,columnspan= 2)
    tabla.heading('#0', text='ID')
    tabla.heading('#1', text='Name')
    tabla.bind('<Double-Button-1>',dobleClipTabla)

    #name
    Label(ventana,text='name').grid(row=2,column=0)
    name = Entry(ventana)
    name.grid(row=2,column=1)
    name.focus()
    #sex
    Label(ventana,text='sex').grid(row=3,column=0)
    sex = Entry(ventana)
    sex.grid(row=3,column=1)
    #qualification
    Label(ventana,text='qualification').grid(row=4,column=0)
    qualification = Entry(ventana)
    qualification.grid(row=4,column=1)

    #name buscar
    Label(ventana,text='find name').grid(row=8,column=0)
    findname = Entry(ventana)
    findname.grid(row=8,column=1)
     #sex buscar
    Label(ventana,text='find sex').grid(row=9,column=0)
    findsex = Entry(ventana)
    findsex.grid(row=9,column=1)
    #qualification buscar
    Label(ventana,text='find qualification').grid(row=10,column=0)
    findqualification = Entry(ventana)
    findqualification.grid(row=10,column=1)
    findD = Button(ventana, text='find', command=findRecord,bg='blue')
    findD.grid(row=11, columnspan=2)

    create = Button(ventana,text='Create',command=createRecord,bg='green',fg='white')
    create.grid(row=5,columnspan=2)
    edit = Button(ventana,text='Edit', command=editarRegistro, bg='yellow')
    edit.grid(row=6,columnspan=2)
    edit['state']='disabled'
    deleteD = Button(ventana, text='Delete', command=deleteRecord,bg='red')
    deleteD.grid(row=7, columnspan=2)
    deleteD['state']='disabled'
    
    showData()

    ventana.mainloop()


