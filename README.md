
- ✅ Registro y autenticación de usuarios
- ✅ Gestión de mascotas (CRUD)
- ✅ Búsqueda de vuelos por origen, destino y fecha
- ✅ Sistema de reservas con verificación de disponibilidad
- ✅ Base de datos con SQLAlchemy
- ✅ Autenticación JWT
- ✅ Documentación automática con Swagger
- ✅ Preparado para despliegue en Render

## Endpoints Principales

### Usuarios
- `POST /usuarios/registro` - Registrar nuevo usuario
- `POST /usuarios/login` - Iniciar sesión

### Mascotas
- `POST /mascotas` - Registrar mascota
- `GET /mascotas` - Obtener mis mascotas

### Vuelos
- `GET /vuelos/buscar?origen=Madrid&destino=Barcelona&fecha=2024-01-15` - Buscar vuelos

### Reservas
- `POST /reservas` - Crear reserva
- `GET /reservas` - Obtener mis reservas

## Documentación

Una vez ejecutada la aplicación, puedes acceder a:
- Documentación Swagger: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

### Usuario
- Información personal (nombre, apellido, email, teléfono)
- Autenticación segura con hash de contraseña
- Relación con mascotas y reservas

### Mascota
- Información de la mascota (nombre, especie, raza, edad, peso)
- Vinculada a un propietario
- Observaciones especiales

### Vuelo
- Información del vuelo (origen, destino, fechas, horarios)
- Precios diferenciados (base + mascota)
- Control de capacidad

### Reserva
- Código único de reserva
- Vincula usuario, vuelo y mascota
- Control de estado y precio total

## Ejemplo de Uso

1. Registrar usuario:
```json
POST /usuarios/registro
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan@email.com",
  "telefono": "+34123456789",
  "password": "mipassword123"
}
```

2. Iniciar sesión:
```json
POST /usuarios/login
{
  "email": "juan@email.com",
  "password": "mipassword123"
}
```

3. Registrar mascota:
```json
POST /mascotas
{
  "nombre": "Max",
  "especie": "perro",
  "raza": "Golden Retriever",
  "edad": 3,
  "peso": 25.5,
  "observaciones": "Muy tranquilo durante los viajes"
}
```

4. Buscar vuelos:
```
GET /vuelos/buscar?origen=Madrid&destino=Barcelona&fecha=2024-01-15
```

5. Crear reserva:
```json
POST /reservas
{
  "vuelo_id": 1,
  "mascota_id": 1,
  "observaciones": "Primera vez que viaja"
}
