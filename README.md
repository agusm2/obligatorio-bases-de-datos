# Obligatorio Bases de Datos

Trabajo obligatorio de Bases de Datos; Mateo Di Fortuna y Agustin Maldonado

## Instructivo para levantar la aplicación (backend + frontend)

Este repositorio contiene dos componentes principales:

- `reserva_salas_api` — API REST hecha con Flask (Python).
- `reserva_salas_ui` — Interfaz web hecha con React + Vite.

A continuación se muestran pasos para levantar cada parte.

### Requisitos

- Python 3.8+ (recomendado Python 3.10/3.11)
- Node.js + npm (para el frontend)
- MySQL

---

## Backend: `reserva_salas_api`

1. Abrir una terminal y situarse en la carpeta del backend:

```bash
cd reserva_salas_api
```

2. Crear y activar un entorno virtual (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
o (en Windows)
python -m venv .venv
.venv/Scripts/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar la API:

```bash
python app.py
```

Por defecto Flask arrancará en http://127.0.0.1:5000/ (modo debug activado en `app.py`).

Rutas de ejemplo:

- GET / → `http://127.0.0.1:5000/` (verifica que la API está viva).
- GET /classroom/ → definido en `reserva_salas_api/routes/salas.py`.

Ejemplo rápido con curl:

```bash
curl http://127.0.0.1:5000/

# Obtiene todas las salas
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/classroom/
```

---

## Frontend: `reserva_salas_ui` (React + Vite)

1. Abrir otra terminal y situarse en la carpeta del frontend:

```bash
cd reserva_salas_ui
```

2. Instalar dependencias (usa npm):

```bash
npm install
```

3. Levantar el servidor de desarrollo:

```bash
npm run dev
```

Por defecto Vite sirve la aplicación en http://localhost:5173/

---

## Probar la integración

1. Levanta primero el backend (`python app.py`).
2. Luego levanta el frontend (`npm run dev`) y abre http://localhost:5173/.
3. Desde el frontend, haz peticiones a `http://127.0.0.1:5000/classroom/...`.
