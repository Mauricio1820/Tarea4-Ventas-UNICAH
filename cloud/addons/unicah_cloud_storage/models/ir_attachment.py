from odoo import models
from odoo.http.stream import Stream


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _to_http_stream(self):
        self.ensure_one()
        if self.type == "binary" and not self.store_fname and self.url:
            data = self.raw.content
            return Stream(
                type="data",
                data=data,
                size=len(data),
                mimetype=self.mimetype,
                download_name=self.name,
                etag=self.checksum,
                public=self.public,
                last_modified=self.write_date,
            )
        return super()._to_http_stream()
