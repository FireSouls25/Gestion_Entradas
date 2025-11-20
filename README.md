# Gestión de Entradas

## Descripción del Proyecto
Este proyecto es un sistema de gestión de eventos y venta de entradas desarrollado con Django. Permite a los organizadores crear y gestionar eventos, definir tipos de entradas, y ver estadísticas. Los asistentes pueden ver tickets y validar entradas si se asignan como asistentes de un evento.

## Requisitos
- Python 3.8+
- pip 
- Git

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/Gestion_Entradas.git
cd Gestion_Entradas
```

### 2. Crear y Activar un Entorno Virtual
Es altamente recomendable usar un entorno virtual para gestionar las dependencias del proyecto.

```bash
python -m venv venv
source .venv/bin/activate  # En linux/mac
venv\Scripts\activate # En Windows
```

### 3. Instalar Dependencias
Instala todas las librerías necesarias usando `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configuración de la Base de Datos
El proyecto utiliza `sqlite3` por defecto, la configuración actual esta dispuesta para render, por lo que no funcionara con SQLite local sin configuración. Si deseas usar SQLite base o PostgreSQL u otra base de datos, configura la variable de entorno `DATABASE_URL` y modifica `Gestion_Entradas/settings.py`.

### 5. Migraciones de la Base de Datos
Aplica las migraciones para crear las tablas de la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Iniciar el Servidor de Desarrollo
```bash
python manage.py runserver
```
El servidor estará disponible en `http://127.0.0.1:8000/`.

## Uso del Sistema

### Roles de Usuario
El sistema define tres roles principales:
- **Organizador**: Puede crear, editar y eliminar eventos, ubicaciones y tipos de tickets. También puede ver estadísticas detalladas de sus eventos y exportar datos.
- **Asistente**: Puede unirse a eventos como asistente, lo que le permite validar entradas para ese evento. 
- **Cliente**: Puede comprar entradas y ver sus tickets.

### Flujo Básico
1.  **Registro/Inicio de Sesión**: Los usuarios pueden registrarse o iniciar sesión.
2.  **Creación de Eventos (Organizador)**: Los organizadores pueden crear eventos y ubicaciones desde su dashboard.
3.  **Compra de Entradas (Cliente/Asistente)**: Los clientes pueden navegar por los eventos y comprar entradas.
4.  **Validación de Entradas (Asistente)**: Los asistentes asignados a un evento pueden validar entradas utilizando un ID de ticket.
5.  **Estadísticas (Organizador)**: Los organizadores pueden ver gráficos y exportar datos de sus eventos.

## Estructura del Proyecto

-   `Gestion_Entradas/`: Configuración principal del proyecto Django.
    -   `settings.py`: Configuración del proyecto.
    -   `urls.py`: Rutas URL principales.
-   `core/`: Aplicación principal (puede contener funcionalidades generales).
-   `dashboard/`: Lógica y plantillas para los dashboards de cada rol.
-   `events/`: Gestión de eventos, ubicaciones y tipos de entrada.
    -   `models.py`: Definición de modelos `Event`, `Location`, `TicketType`.
    -   `views.py`: Vistas para CRUD de eventos, ubicaciones y tipos de entrada, así como la lógica para unirse como asistente.
    -   `urls.py`: Rutas URL específicas de eventos.
    -   `forms.py`: Formularios para eventos, ubicaciones y tipos de entrada.
-   `reports/`: Generación de informes y exportación de datos (e.g., Excel).
    -   `views.py`: Lógica para exportar datos a Excel.
-   `templates/`: Archivos HTML de las plantillas.
    -   `base.html`: Plantilla base del proyecto.
    -   `dashboard/`: Plantillas para los dashboards.
    -   `events/`: Plantillas para eventos, ubicaciones y tipos de entrada.
    -   `tickets/`: Plantillas para compra y visualización de tickets.
    -   `users/`: Plantillas para autenticación y gestión de usuarios.
-   `tickets/`: Gestión de tickets y validación.
    -   `models.py`: Definición del modelo `Ticket`.
    -   `views.py`: Vistas para compra, visualización, generación de QR y validación de tickets.
    -   `urls.py`: Rutas URL específicas de tickets.
-   `users/`: Gestión de usuarios, perfiles y autenticación.
    -   `models.py`: Definición del modelo `UserProfile`.
    -   `views.py`: Vistas para registro, inicio de sesión, configuración y listado de usuarios.
    -   `urls.py`: Rutas URL específicas de usuarios.
-   `static_src/`: Archivos estáticos (CSS, JS) antes de ser compilados por Tailwind.
-   `requirements.txt`: Lista de dependencias de Python.
-   `manage.py`: Utilidad de línea de comandos de Django.

## Modelos Principales

### `events/models.py`
-   **`Location`**: Representa una ubicación física para un evento.
    -   `name` (CharField): Nombre de la ubicación.
    -   `address` (CharField): Dirección de la ubicación.
    -   `capacity` (PositiveIntegerField): Capacidad máxima de personas.
-   **`Event`**: Representa un evento.
    -   `title` (CharField): Título del evento.
    -   `description` (TextField): Descripción detallada.
    -   `start_time` (DateTimeField): Fecha y hora de inicio.
    -   `end_time` (DateTimeField): Fecha y hora de finalización.
    -   `location` (ForeignKey a `Location`): Ubicación del evento.
    -   `organizer` (ForeignKey a `User`): Usuario organizador del evento.
    -   `assistants` (ManyToManyField a `User`): Usuarios que asisten al evento (para validación de tickets).
-   **`TicketType`**: Define un tipo de entrada para un evento.
    -   `name` (CharField): Nombre del tipo de entrada (e.g., "General", "VIP").
    -   `price` (DecimalField): Precio de la entrada.
    -   `quantity` (PositiveIntegerField): Cantidad disponible de este tipo de entrada.
    -   `event` (ForeignKey a `Event`): Evento al que pertenece este tipo de entrada.

### `tickets/models.py`
-   **`Ticket`**: Representa una entrada comprada por un asistente.
    -   `attendee` (ForeignKey a `User`): Usuario que compró la entrada.
    -   `ticket_type` (ForeignKey a `TicketType`): Tipo de entrada comprada.
    -   `purchase_time` (DateTimeField): Fecha y hora de la compra.
    -   `qr_code` (CharField): Código QR asociado a la entrada (para validación).
    -   `is_validated` (BooleanField): Indica si la entrada ha sido validada.

### `users/models.py`
-   **`UserProfile`**: Extiende el modelo `User` de Django para añadir roles.
    -   `user` (OneToOneField a `User`): Relación con el usuario de Django.
    -   `role` (CharField): Rol del usuario (`organizer`, `attendee`, `client`).

## Rutas Principales (URLs)

### `Gestion_Entradas/urls.py`
-   `/`: Redirige al dashboard principal.
-   `/admin/`: Panel de administración de Django.
-   `/users/`: Incluye las rutas de la aplicación `users`.
-   `/events/`: Incluye las rutas de la aplicación `events`.
-   `/tickets/`: Incluye las rutas de la aplicación `tickets`.
-   `/dashboard/`: Incluye las rutas de la aplicación `dashboard`.
-   `/reports/`: Incluye las rutas de la aplicación `reports`.

### `users/urls.py`
-   `/users/login/`: Inicio de sesión.
-   `/users/register/`: Registro de nuevos usuarios.
-   `/users/logout/`: Cierre de sesión.
-   `/users/users/`: Lista de usuarios (clientes y asistentes).
-   `/users/settings/`: Configuración del perfil de usuario.
-   `/users/delete-account/`: Eliminar cuenta.
-   Rutas para restablecimiento de contraseña.

### `events/urls.py`
-   `/events/`: Lista de eventos.
-   `/events/<int:pk>/`: Detalle de un evento.
-   `/events/create/`: Crear nuevo evento (solo organizadores).
-   `/events/<int:pk>/update/`: Editar evento (solo organizadores).
-   `/events/<int:pk>/delete/`: Eliminar evento (solo organizadores).
-   `/events/locations/`: Lista de ubicaciones.
-   `/events/locations/create/`: Crear nueva ubicación (solo organizadores).
-   `/events/locations/<int:pk>/update/`: Editar ubicación (solo organizadores).
-   `/events/locations/<int:pk>/delete/`: Eliminar ubicación (solo organizadores).
-   `/events/event/<int:event_pk>/ticket-types/create/`: Crear tipo de entrada para un evento.
-   `/events/ticket-types/<int:pk>/update/`: Editar tipo de entrada.
-   `/events/ticket-types/<int:pk>/delete/`: Eliminar tipo de entrada.
-   `/events/<int:event_id>/join/`: Unirse a un evento como asistente.
-   `/events/<int:event_id>/cancel-assistance/`: Cancelar asistencia a un evento.

### `tickets/urls.py`
-   `/tickets/<int:ticket_id>/qr/`: Generar código QR para un ticket.
-   `/tickets/<int:ticket_id>/validate/`: Validar un ticket (organizadores y asistentes).
-   `/tickets/event/<int:event_id>/purchase/`: Comprar entradas para un evento.
-   `/tickets/my-tickets/`: Ver mis entradas.
-   `/tickets/my-tickets/event/<int:event_id>/`: Ver mis entradas para un evento específico.
-   `/tickets/<int:ticket_id>/cancel/`: Cancelar la compra de un ticket.

### `dashboard/urls.py`
-   `/dashboard/`: Dashboard principal (redirige según el rol).
-   `/dashboard/event/<int:event_id>/statistics/`: Estadísticas de un evento (solo organizadores).
-   `/dashboard/attendee/event/<int:event_id>/`: Dashboard de asistente para un evento (solo asistentes).

### `reports/urls.py`
-   `/reports/event/<int:event_id>/export/excel/`: Exportar datos de asistentes y estadísticas a Excel (solo organizadores).

## Vistas Genéricas (CRUD)
El proyecto hace uso extensivo de las [vistas genéricas basadas en clases de Django](https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-editing/) para implementar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) de manera eficiente.

-   **`ListView`**: Utilizada para mostrar una lista de objetos (e.g., `EventListView`, `LocationListView`).
-   **`DetailView`**: Utilizada para mostrar los detalles de un solo objeto (e.g., `EventDetailView`).
-   **`CreateView`**: Utilizada para crear nuevos objetos (e.g., `EventCreateView`, `LocationCreateView`, `TicketTypeCreateView`).
-   **`UpdateView`**: Utilizada para editar objetos existentes (e.g., `EventUpdateView`, `LocationUpdateView`, `TicketTypeUpdateView`).
-   **`DeleteView`**: Utilizada para eliminar objetos (e.g., `EventDeleteView`, `LocationDeleteView`, `TicketTypeDeleteView`).

Estas vistas se combinan con `LoginRequiredMixin` y `UserPassesTestMixin` para controlar el acceso basado en el rol del usuario, asegurando que solo los usuarios autorizados puedan realizar ciertas acciones.

## Templates
Las plantillas HTML están estructuradas para ser reutilizables y mantener una interfaz de usuario consistente.

-   **`base.html`**: La plantilla principal que define la estructura básica de la página, incluyendo el encabezado, la barra lateral (responsive) y el área de contenido principal. Todas las demás plantillas extienden esta.
-   **`form_filters.py` (templatetags)**: Un archivo de etiquetas de plantilla personalizado que contiene filtros para aplicar clases CSS de Tailwind a los formularios de Django, facilitando la estilización.
-   Las plantillas están organizadas por aplicación (`dashboard/`, `events/`, `tickets/`, `users/`) para una mejor modularidad.

## Estilización
El proyecto utiliza [Tailwind CSS](https://tailwindcss.com/) para la estilización. Tailwind es un framework CSS "utility-first" que permite construir diseños personalizados directamente en el marcado HTML con clases predefinidas.

-   **Responsive Design**: Se han aplicado clases de Tailwind para asegurar que la interfaz sea completamente responsive, adaptándose a diferentes tamaños de pantalla. La barra lateral se convierte en un menú desplegable en dispositivos móviles.
