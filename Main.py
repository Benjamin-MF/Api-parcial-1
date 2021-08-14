#inicio de la api, importar librerias
from datetime import datetime
import urllib
import os
import sqlalchemy
from pydantic import BaseModel
import databases
from databases import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy import engine
from sqlalchemy import interfaces

from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import FetchedValue
from sqlalchemy.sql.sqltypes import DateTime, Integer, Numeric, String

URL_BASE_DATOS = "postgres://lomoibrthnuiqy:ae19780c359379aa107064daad070080be47fcf0300aa24791e99b90e7449bbd@ec2-18-215-111-67.compute-1.amazonaws.com:5432/d8ic83pdvcuraf"

host_server = os.environ.get('host_server', 'localhost')
puerto_bd = urllib.parse.quote_plus(str(os.environ.get('db_server_port','5432')))
nombre_bd = os.environ.get('database_name','fastapi')
usuario_bd = urllib.parse.quote_plus(str(os.environ.get('db_username','postgres')))
pass_db = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))

metadata = sqlalchemy.MetaData()

#tabla clientes
#nit, nombre, direccion, telefono,
#  contacto, razon social, preferencial, 
# limite_credito, alias, codigo, estado.
clientes = sqlalchemy.table(
    'cliente',
    metadata,
    sqlalchemy.column("id_cliente",sqlalchemy.Integer,primary_key= true),
    sqlalchemy.column("NIT",sqlalchemy.Integer),
    sqlalchemy.column("Nombre",sqlalchemy.String),
    sqlalchemy.column("Direccion",sqlalchemy.String),
    sqlalchemy.column("Telefono",sqlalchemy.Integer),
    sqlalchemy.column("Contacto",sqlalchemy.String),
    sqlalchemy.column("Razon_Social",sqlalchemy.String),
    sqlalchemy.column("Preferencial",sqlalchemy.String),
    sqlalchemy.column("Limite_credito",sqlalchemy.String),
    sqlalchemy.column("Alias",sqlalchemy.String),
    sqlalchemy.column("Estado",sqlalchemy.String),
)


#tabla proveedor
#nit, nombre, direccion, telefono(varios),
#direccion(calle numero comuna ciudad)

proveedor = sqlalchemy.table(
    'proveedor',
    metadata,
    sqlalchemy.column("id_proveedor",sqlalchemy.Integer,primary_key= true),
    sqlalchemy.column("NIT",sqlalchemy.Integer),
    sqlalchemy.column("Nombre_prov",sqlalchemy.String),
    sqlalchemy.column("Direccion_prov",sqlalchemy.String),
    sqlalchemy.column("Telefono_prov",sqlalchemy.Integer),
    sqlalchemy.column("Alias",sqlalchemy.String),
    sqlalchemy.column("Estado",sqlalchemy.String),
)

#tabla de productos
#id_producto, nombre, precio_actual, existencia,
#proveedor, codigo_barras, fecha_vencimiento, lote, fecha_recibido.

productos = sqlalchemy.table(
    'producto',
    metadata,
    sqlalchemy.column("id_producto",sqlalchemy.Integer,primary_key= true),
    sqlalchemy.column("Descripcion_prod",sqlalchemy.String),
    sqlalchemy.column("Precio_actual",sqlalchemy.Numeric),
    sqlalchemy.column("Precio_minimo",sqlalchemy.Numeric),
    sqlalchemy.column("Precio_maximo",sqlalchemy.Numeric),
    sqlalchemy.column("Cant_existencia",sqlalchemy.Integer),
    sqlalchemy.column("Proveedor",sqlalchemy.String),
    sqlalchemy.column("Codigo_barras",sqlalchemy.Integer),
    sqlalchemy.column("Fecha_vencimiento",sqlalchemy.DateTime),
    sqlalchemy.column("Lote",sqlalchemy.Integer),
    sqlalchemy.column("Fecha_recibido",sqlalchemy.DateTime),
)

#Tabla de empleados 
# id_empleado, nombre, apellido, direccion, telefono, 
# salario, puesto, comision, nit, dpi, afiliacion_igss,
#  departamento, estado.

empleados = sqlalchemy.table(
    'empleados',
    metadata,
    sqlalchemy.column("id_empleado",sqlalchemy.Integer,primary_key= true),
    sqlalchemy.column("Nombre",sqlalchemy.String),
    sqlalchemy.column("Apellido",sqlalchemy.String),
    sqlalchemy.column("Direccion",sqlalchemy.String),
    sqlalchemy.column("Telefono_personal",sqlalchemy.Integer),
    sqlalchemy.column("Telefono_oficina",sqlalchemy.Integer),
    sqlalchemy.column("Nombre_contacto_emergencia",sqlalchemy.String),
    sqlalchemy.column("Tel_contacto_emergencia",sqlalchemy.Integer),
    sqlalchemy.column("Salario",sqlalchemy.Numeric),
    sqlalchemy.column("Puesto",sqlalchemy.String),
    sqlalchemy.column("Comision",sqlalchemy.Numeric),
    sqlalchemy.column("NIT",sqlalchemy.Numeric),
    sqlalchemy.column("CUI",sqlalchemy.Numeric),
    sqlalchemy.column("Afiliacion_igss",sqlalchemy.Integer),
    sqlalchemy.column("Departamento",sqlalchemy.String),
    sqlalchemy.column("Estado",sqlalchemy.String),
    
)

engine = sqlalchemy.create_engine(
    URL_BASE_DATOS,pool_size=3, max_overflow=0
)
metadata.create_all(engine)


#clientes
class clientesIn(BaseModel):
    nit:Integer
    nombre:String
    direccion:String
    telefono:Integer
    contacto:String
    razon_social:String
    preferencial:String
    limite_credito:Numeric
    alias:String
    codigo:Integer
    estado:Integer

class clientes(BaseModel):
    id_cliente:Integer
    nit:Integer
    nombre:String
    direccion:String
    telefono:Integer
    contacto:String
    razon_social:String
    preferencial:String
    limite_credito:Numeric
    alias:String
    codigo:Integer
    estado:Integer
    
#proveedores
class proveedorIn(BaseModel):
    nit:Integer
    nombre:String
    direccion:String
    Telefono:Integer
    Alias:String
    Estado:String

class proveedor(BaseModel):
    id_proveedor:Integer
    nit:Integer
    nombre:String
    direccion:String
    Telefono:Integer
    Alias:String
    Estado:String

#productos
class productoIn(BaseModel):
    descripcion:String
    precio_actual:Numeric
    Precio_minimo:Numeric
    Precio_maximo:Numeric
    cant_existencia:Integer
    proveedor:String
    codigo_barras:Integer
    FetchedValue:DateTime
    lote:Integer
    Fecha_recibido:datetime

class producto(BaseModel):
    id_producto:Integer
    descripcion:String
    precio_actual:Numeric
    Precio_minimo:Numeric
    Precio_maximo:Numeric
    cant_existencia:Integer
    proveedor:String
    codigo_barras:Integer
    FetchedValue:DateTime
    lote:Integer
    Fecha_recibido:datetime

#empleados
class empleadoIn(BaseModel):
    Nombre:String
    Apellido:String
    direccion:String
    telefono_personal:Integer
    telefono_oficina:Integer
    nombre_contacto_emergencia:String
    tel_contacto_emergencia:Integer
    Salario:Numeric
    puesto:String
    comision:Numeric
    nit:Integer
    cui:Integer
    afiliacion_igss:Integer
    departamento:String
    Estado:String

class empleado(BaseModel):
    id_empleado:Integer
    Nombre:String
    Apellido:String
    direccion:String
    telefono_personal:Integer
    telefono_oficina:Integer
    nombre_contacto_emergencia:String
    tel_contacto_emergencia:Integer
    Salario:Numeric
    puesto:String
    comision:Numeric
    nit:Integer
    cui:Integer
    afiliacion_igss:Integer
    departamento:String
    Estado:String

app = FastAPI(title="api parcial")
app.add_middleware(
        CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = databases.Database(URL_BASE_DATOS)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnet()

    
#empleados
@app.post("/empleados/",response_model=empleado)
async def create_empleado(emp:empleadoIn):
    query= empleado.insert().values(nombre=emp.nombre,apellido=emp.apellido, direccion = emp.direccion, telefono = emp.telefono_personal, tel_oficina = emp.telefono_oficina, nom_contac_emergencia = emp.nombre_contacto_emergencia, 
    tel_contac_emergencia = emp.tel_contacto_emergencia, salario = emp.Salario,
    puesto = emp.puesto, comision = emp.comision, nit = emp.nit, cui = emp.cui, afiliacion_igss = emp.afiliacion_igss,
    departamento = emp.departamento, estado = emp.Estado)
    
    last_record_id =await database.execute(query)
    return {**emp.dict(), "id":last_record_id}

@app.get("/getEmpleado/",response_model=List[empleado] )
async def getEmpleado(skip: int=0, take: int=20):
    query= empleado.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@app.get("/getEmpleado/{empleado_id}",response_model=empleado)
async def getEmpleadoId(emp_id: int ):
    query= empleado.select().where(empleado.c.id==emp_id  )
    return await database.fetch_one(query)

@app.delete("/empleadoDelete/{empleado_id}/")
async def del_empleado(emp_id: int):
    query = empleado.delete().where(empleado.c.id==emp_id)
    await database.execute(query)
    return {"message":" Empleado with id:{} deleted succesfully!".format(emp_id)}

@app.put("/empleadoUpdate/{emp_id}",response_model=empleado)
async def setEmpleadoId(emp_id: int,emp:empleadoIn):
    query = empleado.update().where(empleado.c.id==emp_id).values(nombre=emp.nombre, apellido=emp.apellido,status=emp.status)
    await database.execute(query)
    return {**emp.dict(),"id":emp_id}

