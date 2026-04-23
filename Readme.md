# Licium - (Niveles 2, 3 y 4)

Este repositorio contiene el desarrollo de tres módulos funcionales para el framework **Licium**, enfocados en la gestión de inventario, moderación de feedback y organización de eventos.

El desarrollo se divide en tres capas:

### 1. Nivel 2: Gestión de activos (`asset_lending`)
* **Objetivo:** Controlar el préstamo y devolución de activos físicos.
* **Lógica implementada:**
    * Modelo de datos para Activos (`Asset`) y Préstamos (`Loan`).
    * Servicios automatizados para cambiar el estado del activo (Disponible/Prestado) al procesar un préstamo.
    * Validación de fechas de devolución.

### 2. Nivel 3: Moderación de feedback (`feedback_moderation`)
* **Objetivo:** Crear un canal de sugerencias con flujo de aprobación.
* **Lógica implementada:**
    * Sistema de estados: `Pendiente`, `Publicado` y `Rechazado`.
    * **Seguridad ACL:** Configuración de reglas para que los usuarios anónimos solo vean sugerencias "Publicadas", mientras que los moderadores gestionan todo el flujo.
    * Acciones de servicio expuestas para la transición de estados.

### 3. Nivel 4: Eventos comunitarios (`community_events`)
* **Objetivo:** Gestión integral de eventos con control de aforo y configuración dinámica.
* **Lógica implementada:**
    * **Inscripción inteligente:** Servicio que valida el aforo máximo (`capacity`) antes de permitir un registro.
    * **Settings dinámicos:** Uso de `settings.yml` para configurar parámetros globales del módulo sin tocar el código.
    * Interfaz avanzada con botones de acción personalizados (`row_actions`).

---

## Nota sobre el despliegue
Durante el desarrollo en el entorno de contenedores, se identificó un conflicto de integridad (`UniqueViolation`) en el módulo `admin` del núcleo de Licium tras la instalación inicial vía API. 

**Estado del código:**
* **Backend:** 100% funcional. Los modelos, servicios y controladores están correctamente definidos y vinculados.
* **Base de Datos:** Tablas y registros de semillas (`seeds`) inyectados con éxito.
* **UI:** Los menús y botones son visibles, aunque la respuesta del servidor puede devolver `404` en ciertos endpoints debido a que el cargador de rutas de Licium requiere una instalación limpia del núcleo para mapear nuevos módulos.

---

## Tecnologías utilizadas
* **Python 3.13** (FastAPI / SQLAlchemy)
* **YAML** (Definición de vistas y seguridad en Licium)
* **PostgreSQL**
* **Docker**