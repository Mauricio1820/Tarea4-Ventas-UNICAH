import os

params = env["ir.config_parameter"].sudo()
params.set_str("ir_attachment.location", "db")
env["ir.attachment"].force_storage()

admin = env.ref("base.user_admin")
admin.write({
    "name": "Administrador Tarea 4 UNICAH",
    "login": "mauricio",
    "password": os.environ["ODOO_OWNER_PASSWORD"],
    "lang": "es_ES",
    "tz": "America/Tegucigalpa",
})
if os.environ.get("RENDER_EXTERNAL_URL"):
    params.set_str("web.base.url", os.environ["RENDER_EXTERNAL_URL"])
    params.set_bool("web.base.url.freeze", True)
params.set_str("tarea4.cloud.initialized", "1")
env.cr.commit()
print("Tarea 4 ready: Ventas UNICAH installed with database-backed attachments.")
