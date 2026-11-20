from odoo import Command

params = env["ir.config_parameter"].sudo()
if params.get_str("tarea4.demo.initialized") != "1":
    company = env.company.sudo()
    currency = env.ref("base.HNL").sudo()
    currency.write({"active": True})
    company.write({"currency_id": currency.id, "country_id": env.ref("base.hn").id})

    pricelist = env["product.pricelist"].sudo().search([
        ("name", "=", "Precios HNL - Tarea 4"),
        ("company_id", "=", company.id),
    ], limit=1)
    if not pricelist:
        pricelist = env["product.pricelist"].sudo().create({
            "name": "Precios HNL - Tarea 4",
            "currency_id": currency.id,
            "company_id": company.id,
        })
    else:
        pricelist.write({"currency_id": currency.id})

    product = env["product.template"].sudo().search([
        ("name", "=", "Laptop Dell Latitude"),
    ], limit=1)
    if not product:
        product = env["product.template"].sudo().create({
            "name": "Laptop Dell Latitude",
            "list_price": 30000,
            "sale_ok": True,
        })
    else:
        product.write({"list_price": 30000, "sale_ok": True})
    variant = product.product_variant_id.sudo()
    variant.with_company(company).write({"standard_price": 22000})

    partner = env["res.partner"].sudo().search([
        ("name", "=", "Cliente de Prueba UNICAH"),
    ], limit=1)
    if not partner:
        partner = env["res.partner"].sudo().create({
            "name": "Cliente de Prueba UNICAH",
            "is_company": True,
            "canal_preferido": "tienda",
        })
    else:
        partner.write({"canal_preferido": "tienda"})

    order = env["sale.order"].sudo().search([
        ("client_order_ref", "=", "TAREA4-DEMO-60000"),
    ], limit=1)
    if not order:
        order = env["sale.order"].sudo().create({
            "partner_id": partner.id,
            "company_id": company.id,
            "pricelist_id": pricelist.id,
            "canal_venta": "tienda",
            "client_order_ref": "TAREA4-DEMO-60000",
            "order_line": [Command.create({
                "product_id": variant.id,
                "product_uom_qty": 2,
                "price_unit": 30000,
                "name": "Laptop Dell Latitude",
            })],
        })

    env.flush_all()
    print("Tarea 4 demo:", order.name, "HNL", order.amount_total,
          "units", order.total_unidades,
          "requires approval", order.requiere_aprobacion, flush=True)
    params.set_str("tarea4.demo.initialized", "1")
    env.cr.commit()
