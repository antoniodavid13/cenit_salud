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
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    try:
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
    except Exception as e:
        # Aquí puedes imprimir el error en consola para saber qué falló
        print(f"Error detectado: {e}")
        
        # Devolvemos la página 404 (o una de 500 Error Interno)
        return templates.TemplateResponse(
            "pages/404.html", 
            {"request": request},
            status_code=404
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
def post_nuevo_medico(request: Request, nombre: str = Form(...), especialidad: str = Form(...), email: str = Form(...)):
    try:
        # Tu validación de Pydantic existente...
        medico_data = MedicoCreate(nombre=nombre, especialidad=especialidad, email=email)
        
        # Intentamos insertar
        insert_medico(medico_data.nombre, medico_data.especialidad, medico_data.email)
        return RedirectResponse(url="/", status_code=303)
        
    except ValueError as e:
        # Aquí capturamos el error del correo duplicado
        return templates.TemplateResponse(
            "pages/nuevo_medico.html",
            {
                "request": request,
                "errores": [str(e)],
                "nombre": nombre,
                "especialidad": especialidad,
                "email": email
            },
            status_code=400
        )

# --- GET: Cargar formulario de edición ---
@app.get("/medico/editar/{medico_id}", response_class=HTMLResponse)
def get_editar_medico(request: Request, medico_id: int):
    row = fetch_medico_by_id(medico_id)
    if not row:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    medico = map_row_to_medico(row)
    return templates.TemplateResponse("pages/editar_medico.html", {
        "request": request,
        "medico": medico,
        "errores": None
    })

# --- POST: Procesar la edición ---
@app.post("/medico/editar/{medico_id}")
def post_editar_medico(
    request: Request,
    medico_id: int,
    nombre: str = Form(...),
    especialidad: str = Form(...),
    email: str = Form(...)
):
    try:
        # 1. Validar formato con Pydantic
        medico_valido = MedicoUpdate(nombre=nombre, especialidad=especialidad, email=email)
        
        # 2. Actualizar en DB (aquí puede saltar el ValueError del correo)
        update_medico(medico_id, medico_valido.nombre, medico_valido.especialidad, medico_valido.email)
        
        return RedirectResponse(url="/#doctores", status_code=303)

    except (ValidationError, ValueError) as e:
        # Capturamos ambos tipos de errores
        if isinstance(e, ValidationError):
            errores = [f"{err['loc'][0].capitalize()}: {err['msg']}" for err in e.errors()]
        else:
            # Es el ValueError de la base de datos
            errores = [str(e)]
            
        return templates.TemplateResponse("pages/editar_medico.html", {
            "request": request,
            # Importante: pasar el ID correcto para que el formulario sepa a quién editar si falla
            "medico": {"id": medico_id, "nombre": nombre, "especialidad": especialidad, "email": email},
            "errores": errores
        })

# --- DELETE: Borrar médico ---
@app.delete("/medico/eliminar/{medico_id}")
def endpoint_eliminar_medico(medico_id: int):
    exito = delete_medico(medico_id)
    if exito:
        return {"ok": True}
    return JSONResponse(status_code=404, content={"ok": False, "message": "No se encontró el médico"})