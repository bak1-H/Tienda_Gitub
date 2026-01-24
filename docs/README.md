# Proyecto Flask Actualizado

Breve descripción
------------------
Pequeña tienda creada con Flask. La aplicación funciona con SQLite por defecto (archivo local `local.db`) o puede conectarse a PostgreSQL mediante la variable de entorno `DATABASE_URL`. El código desplegable está en la carpeta `flask-oc` y el entrypoint para producción con gunicorn es `run:app` (ver `flask-oc/run.py`).

Requisitos
---------
- Python 3.11
- `pip` y un entorno virtual (recomendado)
- PostgreSQL (opcional; recomendado para producción en Render) o SQLite local

Instalación y ejecución local
----------------------------
PowerShell (recomendado en Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Establecer SECRET_KEY temporal (solo para desarrollo)
$env:SECRET_KEY = "dev-secret"
# Ejecutar desde el directorio del servicio
cd flask-oc
python run.py
```

cmd.exe (Windows):

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
set SECRET_KEY=dev-secret
cd flask-oc
python run.py
```

Notas:
- Al ejecutar `python flask-oc/run.py` la app arranca en modo debug cuando se lanza localmente.
- Si prefieres usar un archivo `.env`, crea uno en la raíz con las variables `SECRET_KEY` y `DATABASE_URL`.

Variables de entorno y `.env`
-----------------------------
La app lee estas variables:
- `SECRET_KEY` (requerida para sesiones)
- `DATABASE_URL` (opcional — si no está, se usa `sqlite:///local.db` según `flask-oc/app/config.py`)

Ejemplo `.env`:

```
SECRET_KEY=dev-secret
DATABASE_URL=postgresql://usuario:password@localhost:5432/mitienda
```

Rutas útiles
------------
- Crear usuario administrador (seed): `/auth/seed` — crea `admin/admin` (respuesta simple `ok`).
- Login: `/auth/login`
- Menú / órdenes: `/` (gestionado en `flask-oc/app/main.py` y `flask-oc/app/orders.py`)

Despliegue en Render (resumen)
----------------------------
1. Crear una base de datos PostgreSQL gestionada en Render (Render → New → PostgreSQL) y copiar la `DATABASE_URL` provista.
2. Crear un Web Service en Render o usar `render.yaml` incluido:
   - Root directory: `flask-oc`
   - Build command: `pip install -r requirements.txt`
   - Start command: `cd flask-oc && gunicorn run:app --bind 0.0.0.0:$PORT`
   - Environment: añadir `SECRET_KEY` y `DATABASE_URL` en las env vars del servicio.
3. (Opcional) CI/CD: añadir `RENDER_TOKEN` y `RENDER_SERVICE_ID` a los Secrets de GitHub para que el workflow en `flask-oc/.github/workflows/ci-cd.yaml` pueda gatillar despliegues.

Notas técnicas y recomendaciones
-------------------------------
- Entry point: en `flask-oc/run.py` la variable `app` se crea con `create_app()` — por eso `gunicorn run:app` funciona cuando el directorio actual es `flask-oc`.
- Fallback DB: si `DATABASE_URL` no está definida, la app usa `sqlite:///local.db` (ver `flask-oc/app/config.py`).
- Seed: la ruta `/auth/seed` crea un usuario `admin` con password `admin` para desarrollo; no usar en producción sin protección.
- Precios y totales: en los modelos (`flask-oc/app/models.py`) los precios y totales se almacenan como enteros (centavos). Es una consideración para presentar/parsear valores en la interfaz o al insertar datos.
- IVA: la factura usa una tasa por defecto `0.19` (19%).

Solución de problemas
---------------------
- Si la app no se conecta a la DB en Render, revisa los logs del servicio en Render y confirma que `DATABASE_URL` está correcta.
- Para entornos de desarrollo, prueba primero con SQLite local para descartar problemas con la cadena de conexión a Postgres.

Archivos clave
-------------
- Entrypoint: `flask-oc/run.py`
- Configuración: `flask-oc/app/config.py`
- Modelos: `flask-oc/app/models.py`
- Autenticación/seed: `flask-oc/app/auth.py`
- Despliegue plantilla: `render.yaml`

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

## Arquitectura del Sistema
- App Flask: `run.py` (entry) y carpeta `app/` con módulos.
- Módulos:
   - `auth.py`: Login/Logout y Registro.
   - `orders.py`: RF1 y RF3 (crear y listar órdenes).
   - `invoices.py`: RF4 (emitir factura, IVA 19%).
   - `shipments.py`: RF5 (despacho con nota).
   - `models.py`: ORM SQLAlchemy (User, Order, Product, OrderItem, Invoice, Shipment).
   - `main.py`: Factory `create_app`, registra blueprints y ejecuta `db.create_all()`.
- Templates: Bootstrap en `templates/` (`base`, `login`, `register`, `menu`, `new_order`, `invoice`).
- Persistencia: PostgreSQL (o SQLite local). Conexión vía `SQLAlchemy`.

## Base de Datos (DER y físico)
- Entidades:
   - `User(id, username, password_hash)`
   - `Order(id, order_number, customer_name, address, phone, commune, region, status, created_at)`
   - `Product(id, name, price)`
   - `OrderItem(id, order_id FK, product_id FK, quantity)`
   - `Invoice(id, order_id FK unique, iva_rate, total_net, total_iva, total_with_tax, created_at)`
   - `Shipment(id, invoice_id FK, note, dispatched_at)`
- Relaciones:
   - `Order 1..* OrderItem` (una orden tiene múltiples ítems).
   - `Order 1..1 Invoice` (una orden tiene una factura).
   - `Invoice 1..1 Shipment` (despacho asociado a factura).
- Diagrama (texto):
   - User (login)
   - Order ──< OrderItem >── Product
   - Order ──1:1── Invoice ──1:1── Shipment

Notas:
- `order_number` es único para evitar duplicados.
- Totales de `Invoice` se calculan a partir de `OrderItem` + IVA 19%.

## Flujo del Sistema (OC → Factura → Despacho)
1. Ingreso OC (RF1): Usuario autenticado crea Orden con datos de cliente y productos.
2. Menú (RF3): Lista órdenes, permite facturar o ver detalle.
3. Emisión de Factura (RF4): Seleccionar OC → calcular neto + IVA 19% → guardar `Invoice` y cambiar estado a "facturada".
4. Despacho (RF5): Desde la factura → marcar despachado con nota → crear `Shipment` y estado "despachada" en la OC.
5. Login/Logout (RF2): Control de acceso al menú y acciones.

## Conclusiones y cierre
- Aprendizajes: 
   - Uso de Flask + SQLAlchemy + Flask-Login.
   - Cálculo de IVA y persistencia de estados.
   - Despliegue en Render (Blueprint vs Web Service) y CI/CD básico.
- Dificultades:
   - Configurar `DATABASE_URL` con `psycopg` v3 (`postgresql+psycopg://`).
   - Rutas de build/start en Render cuando el proyecto está en subcarpeta.
   - Evitar duplicados en `order_number` y manejar errores de integridad.
- Mejoras:
   - Validaciones más completas (precio/cantidad, formularios WTForms).
   - Migraciones con Alembic y pruebas unitarias/integración.
   - Roles de usuario (admin/operador) y paginación en listado.
   - N° de factura amigable (ej: `F-000123`) derivado del `id`.

Notas:
- El número de orden es único. Si repites, verás un mensaje: "Número de orden ya existe".
- Los productos aceptan nombre, precio y cantidad. Las líneas vacías se omiten.

## Despliegue en Render
- Crear servicio Web en Render con `render.yaml`.
- Variables: `SECRET_KEY`, `DATABASE_URL`.
- Agregar `RENDER_TOKEN` y `RENDER_SERVICE_ID` como secrets en GitHub para el workflow.
- El workflow usa la API de Render para gatillar el deploy del servicio existente.

## Manual de Usuario
- Consulta el manual paso a paso en `docs/user-manual.md`.
- Contiene: acceso, creación de órdenes, facturación, despacho, estados, y solución de problemas.
