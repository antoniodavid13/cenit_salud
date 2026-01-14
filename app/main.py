from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional, List
import re

# Importamos las funciones que consultan/insertan/eliminan en MySQL
from app.database import (
    fetch_all_medicos, 
    insert_medico, 
    delete_medico,
    fetch_cliente_by_id,
    update_cliente
)


# Modelo base con validaciones comunes
class ClienteBase(BaseModel):
    nombre: str
    especilidad: str
    email: EmailStr
    
    @field_validator('nombre','especilidad')
    @classmethod
    def validar_nombre_apellido(cls, v: str) -> str:
        """Valida que nombre y apellido tengan formato correcto."""
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        
        v = v.strip()
        
        if len(v) < 2:
            raise ValueError('Debe tener al menos 2 caracteres')
        
        if len(v) > 50:
            raise ValueError('No puede exceder 50 caracteres')
        
        # Solo letras, espacios, tildes y caracteres especiales del español
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', v):
            raise ValueError('Solo se permiten letras y espacios')
        
        return v.title()  # Capitaliza cada palabra
    


# Modelo para lectura de BD (sin validaciones estrictas, acepta datos históricos)
class ClienteDB(BaseModel):
    id: int
    nombre: str
    especilidad: str
    email: str



# Modelo para crear cliente (sin ID)
class ClienteCreate(ClienteBase):
    pass


# Modelo para actualizar cliente (sin ID)
class ClienteUpdate(ClienteBase):
    pass


# Modelo completo de Cliente (con ID y validaciones)
class Cliente(ClienteBase):
    id: int


app = FastAPI(title="SumaAPI")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas
templates = Jinja2Templates(directory="app/templates")


def map_rows_to_medicos(rows: List[dict]) -> List[ClienteDB]:
    """
    Convierte las filas del SELECT * FROM clientes (dict) 
    en objetos ClienteDB (sin validaciones estrictas para datos existentes).
    """
    return [
        ClienteDB(
            id=row["id_medico"],
            nombre=row["nombre"],
            especilidad=row["especialidad"],
            email=row["correo_interno"],
        )
        for row in rows
    ]


# --- GET principal ---
@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    # 1️⃣ Obtenemos los datos desde MySQL
    rows = fetch_all_medicos()

    # 2️⃣ Convertimos cada fila a Cliente (valida estructura)
    medicos = map_rows_to_medicos(rows)

    # 3️⃣ Enviamos a la plantilla
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "medicos": medicos
        }
    )


# --- GET formulario nuevo cliente ---
@app.get("/medico/nuevo", response_class=HTMLResponse)
def get_nuevo_medico(request: Request):
    return templates.TemplateResponse(
        "pages/nuevo_medico.html",
        {
            "request": request,
            "mensaje": None
        }
    )


# --- POST guardar nuevo cliente ---
@app.post("/medico/nuevo")
def post_nuevo_medico(
    request: Request,
    nombre: str = Form(...),
    especialidad: str = Form(...),
    email: str = Form(...)
):
    try:
        # Validamos los datos usando Pydantic
        cliente_data = ClienteCreate(
            nombre=nombre,
            especialidad=especialidad,
            email=email
        )
        
        # Insertamos el cliente en la base de datos
        insert_medico(
            cliente_data.nombre,
            cliente_data.especialidad,
            cliente_data.email,
        )
        
        # Redirigimos al inicio para ver el listado actualizado
        return RedirectResponse(url="/", status_code=303)
        
    except ValidationError as e:
        # Extraemos los errores de validación
        errores = []
        for error in e.errors():
            campo = str(error['loc'][0]) if error['loc'] else 'campo'
            mensaje = error['msg']
            errores.append(f"{campo.capitalize()}: {mensaje}")
        
        # Mostramos el formulario con los errores
        return templates.TemplateResponse(
            "pages/nuevo_cliente.html",
            {
                "request": request,
                "mensaje": None,
                "errores": errores,
                "nombre": nombre,
                "especialidad": especialidad,
                "correo_interno": email
            },
            status_code=422
        )


# --- DELETE eliminar cliente ---
@app.delete("/medico/{cliente_id}")
def delete_cliente_endpoint(cliente_id: int):
    """
    Endpoint para eliminar un cliente por su ID.
    """
    eliminado = delete_medico(cliente_id)
    
    if not eliminado:
        raise HTTPException(status_code=404, detail="Medico no encontrado")
    
    return JSONResponse(
        content={"mensaje": "Medico eliminado exitosamente"},
        status_code=200
    )


# --- GET formulario editar cliente ---
@app.get("/medico/editar/{cliente_id}", response_class=HTMLResponse)
def get_editar_cliente(request: Request, cliente_id: int):
    """
    Endpoint para mostrar el formulario de edición con datos precargados.
    """
    # Obtenemos los datos del cliente
    cliente_data = fetch_cliente_by_id(cliente_id)
    
    if not cliente_data:
        raise HTTPException(status_code=404, detail="Medico no encontrado")
    
    # Convertimos a modelo ClienteDB para mostrar en formulario (sin validaciones)
    cliente = ClienteDB(**cliente_data)
    
    return templates.TemplateResponse(
        "pages/editar_medico.html",
        {
            "request": request,
            "medico": cliente
        }
    )


# --- POST actualizar cliente ---
@app.post("/medico/editar/{cliente_id}")
def post_editar_cliente(
    request: Request,
    cliente_id: int,
    nombre: str = Form(...),
    especialidad: str = Form(...),
    email: str = Form(...)
):
    """
    Endpoint para actualizar los datos de un cliente.
    """
    try:
        # Validamos los datos usando Pydantic
        cliente_data = ClienteUpdate(
            nombre=nombre,
            especialidad=especialidad,
            email=email
        )
        
        # Actualizamos el cliente en la base de datos
        actualizado = update_cliente(
            cliente_id,
            cliente_data.nombre,
            cliente_data.especialidad,
            cliente_data.email,
        )
        
        if not actualizado:
            raise HTTPException(status_code=404, detail="Medico no encontrado")
        
        # Redirigimos al inicio para ver el listado actualizado
        return RedirectResponse(url="/", status_code=303)
        
    except ValidationError as e:
        # Extraemos los errores de validación
        errores = []
        for error in e.errors():
            campo = str(error['loc'][0]) if error['loc'] else 'campo'
            mensaje = error['msg']
            errores.append(f"{campo.capitalize()}: {mensaje}")
        
        # Creamos un objeto cliente temporal para mostrar en el formulario
        cliente_temp = ClienteDB(
            id=cliente_id,
            nombre=nombre,
            especialidad=especialidad,
            email=email,
        )
        
        # Mostramos el formulario con los errores
        return templates.TemplateResponse(
            "pages/editar_medico.html",
            {
                "request": request,
                "cliente": cliente_temp,
                "errores": errores
            },
            status_code=422
        )
