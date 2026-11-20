# Despliegue de Tarea 4 en Render

Esta carpeta contiene únicamente la infraestructura para ejecutar Odoo 20 y el módulo original de `custom_addons/ventas_unicah` con PostgreSQL de Neon.

Odoo usa las variables `DATABASE_URL`, `ODOO_MASTER_PASSWORD` y `ODOO_OWNER_PASSWORD` suministradas de forma privada en Render. Los recursos de Odoo se guardan en PostgreSQL, pues Render Free no cuenta con almacenamiento persistente. El arranque instala el módulo si la base todavía no ha sido inicializada.

El usuario de Odoo es `mauricio`. La ruta para verificar el servidor es `/web/health`.

Los archivos originales de la Tarea 4 permanecen intactos en `custom_addons`.
