FROM odoo:20.0-20261112
USER root
COPY --chown=odoo:odoo custom_addons/ /mnt/extra-addons/
COPY --chown=odoo:odoo cloud/addons/ /mnt/extra-addons/
COPY --chown=odoo:odoo cloud/start.py /opt/tarea4/start.py
COPY --chown=odoo:odoo cloud/bootstrap.py /opt/tarea4/bootstrap.py
USER odoo
EXPOSE 8069
ENTRYPOINT ["/usr/bin/python3", "/opt/tarea4/start.py"]
