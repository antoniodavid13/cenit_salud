from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional, List
import re

from app.database import (
    fetch_all_medicos, 
    insert_medico, 
    delete_medico,
    fetch_medico_by_id,
    update_medico
)


# ==================== MODELOS PYDANTIC ====================

class MedicoBase(BaseModel):
    """Modelo base con validaciones para médicos"""
    nombre: str
    especialidad: str
    email: EmailStr
    
    @field_validator('nombre', 'especialidad')
    @classmethod
    def validar_campos_texto(cls, v: str) -> str:
        """Valida que nombre y especialidad tengan formato correcto."""
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
        
        return v.title()


class MedicoCreate(MedicoBase):
    """Modelo para crear médico (sin ID)"""
    pass


class MedicoUpdate(MedicoBase):
    """Modelo para actualizar médico (sin ID)"""
    pass


class MedicoDB(BaseModel):
    """Modelo para lectura de BD (sin validaciones estrictas)"""
    id: int
    nombre: str
    especialidad: str
    email: str


# ==================== CONFIGURACIÓN FASTAPI ====================

app = FastAPI(title="VitaClinic API")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas Jinja2
templates = Jinja2Templates(directory="app/templates")


# ==================== FUNCIONES AUXILIARES ====================

def map_rows_to_medicos(rows: List[dict]) -> List[MedicoDB]:
    """
    Convierte las filas del SELECT de medicos (dict) 
    en objetos MedicoDB.
    """
    return [
        MedicoDB(
            id=row["id_medico"],
            nombre=row["nombre"],
            especialidad=row["especialidad"],
            email=row["correo_interno"],
        )
        for row in rows
    ]


def map_row_to_medico(row: dict) -> MedicoDB:
    """
    Convierte una fila individual a MedicoDB.
    """
    return MedicoDB(
        id=row["id_medico"],
        nombre=row["nombre"],
        especialidad=row["especialidad"],
        email=row["correo_interno"],
    )


# ==================== ENDPOINTS ====================

# --- GET página principal ---
@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    """Página principal con listado de médicos."""
    rows = fetch_all_medicos()
    medicos = map_rows_to_medicos(rows)
    
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "medicos": medicos
        }
    )


# --- GET formulario nuevo médico ---
@app.get("/medico/nuevo", response_class=HTMLResponse)
def get_nuevo_medico(request: Request):
    """Muestra formulario para crear nuevo médico."""
    return templates.TemplateResponse(
        "pages/nuevo_medico.html",
        {
            "request": request,
            "errores": None
        }
    )


# --- POST guardar nuevo médico ---
@app.post("/medico/nuevo")
def post_nuevo_medico(
    request: Request,
    nombre: str = Form(...),
    especialidad: str = Form(...),
    email: str = Form(...)
):
    """Procesa el formulario y guarda nuevo médico."""
    try:
        # Validamos los datos usando Pydantic
        medico_data = MedicoCreate(
            nombre=nombre,
            especialidad=especialidad,
            email=email
        )
        
        # Insertamos en la base de datos
        insert_medico(
            medico_data.nombre,
            medico_data.especialidad,
            medico_data.email
        )
        
        # Redirigimos al inicio
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
            "pages/nuevo_medico.html",
            {
                "request": request,
                "errores": errores,
                "nombre": nombre,
                "especialidad": especialidad,
                "email": email
            },
            status_code=422
        )


# --- GET formulario editar médico ---
@app.get("/medico/editar/{medico_id}", response_class=HTMLResponse)
def get_editar_medico(request: Request, medico_id: int):
    """Muestra formulario de edición con datos precargados."""
    medico_data = fetch_medico_by_id(medico_id)
    
    if not medico_data:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    medico = map_row_to_medico(medico_data)
    
    return templates.TemplateResponse(
        "pages/editar_medico.html",
        {
            "request": request,
            "medico": medico,
            "errores": None
        }
    )


# --- POST actualizar médico ---
@app.post("/medico/editar/{medico_id}")
def post_editar_medico(
    request: Request,
    medico_id: int,
    nombre: str = Form(...),
    especialidad: str = Form(...),
    email: str = Form(...)
):
    """Procesa el formulario y actualiza el médico."""
    try:
        # Validamos los datos usando Pydantic
        medico_data = MedicoUpdate(
            nombre=nombre,
            especialidad=especialidad,
            email=email
        )
        
        # Actualizamos en la base de datos
        actualizado = update_medico(
            medico_id,
            medico_data.nombre,
            medico_data.especialidad,
            medico_data.email
        )
        
        if not actualizado:
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        
        # Redirigimos al inicio
        return RedirectResponse(url="/", status_code=303)
        
    except ValidationError as e:
        # Extraemos los errores de validación
        errores = []
        for error in e.errors():
            campo = str(error['loc'][0]) if error['loc'] else 'campo'
            mensaje = error['msg']
            errores.append(f"{campo.capitalize()}: {mensaje}")
        
        # Creamos objeto temporal para mostrar en el formulario
        medico_temp = MedicoDB(
            id=medico_id,
            nombre=nombre,
            especialidad=especialidad,
            email=email
        )
        
        return templates.TemplateResponse(
            "pages/editar_medico.html",
            {
                "request": request,
                "medico": medico_temp,
                "errores": errores
            },
            status_code=422
        )


# --- DELETE eliminar médico ---
@app.delete("/medico/{medico_id}")
def delete_medico_endpoint(medico_id: int):
    """Endpoint para eliminar un médico por su ID."""
    eliminado = delete_medico(medico_id)
    
    if not eliminado:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    return JSONResponse(
        content={"mensaje": "Médico eliminado exitosamente"},
        status_code=200
    )