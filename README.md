# Proyecto Flask Actualizado


## Requisitos
- Python 3.11
- Base de datos: PostgreSQL (usa `DATABASE_URL`) o SQLite local por defecto.
- Archivo `.env` opcional (cargado automáticamente) para `SECRET_KEY` y `DATABASE_URL`.

## Instalación
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY = "dev-secret"
# Ejemplo Postgres: $env:DATABASE_URL = "postgresql://usuario:pass@host:5432/db"
python run.py
```
Abrir `http://localhost:5000/auth/seed` para crear usuario `admin/admin`.
Luego ir a `http://localhost:5000/auth/login`.

### Usando `.env` (recomendado)
Crea un archivo `.env` en la raíz del proyecto:
```
SECRET_KEY=dev-secret
DATABASE_URL=postgresql://usuario:password@localhost:5432/mitienda
```
La app carga `.env` automáticamente.

## Funcionalidades
- RF1: Crear orden con cliente y productos.
- RF2: Login simple con Flask-Login.
- RF3: Menú lista órdenes, Home y Cerrar sesión.
- RF4: Factura calcula IVA 19% y total; cambia estado a "facturada".
- RF5: Despacho marca como "despachada" y guarda nota.
- RF6: CI/CD con GitHub Actions y despliegue a Render.

Notas:
- El número de orden es único. Si repites, verás un mensaje: "Número de orden ya existe".
- Los productos aceptan nombre, precio y cantidad. Las líneas vacías se omiten.

## Despliegue en Render
- Crear servicio Web en Render con `render.yaml`.
- Variables: `SECRET_KEY`, `DATABASE_URL`.
- Agregar `RENDER_TOKEN` y `RENDER_SERVICE_ID` como secrets en GitHub para el workflow.
- El workflow usa la API de Render para gatillar el deploy del servicio existente.

## Nota estudiante
- Código está comentado de forma básica.
 - Si tu contraseña tiene espacios, en `DATABASE_URL` usa `%20` (ej: `cisco%20123`).
