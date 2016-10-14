import odoorpc
import progressbar
import logging
import sys
import traceback
odoo = odoorpc.ODOO('source_server', port=8069)
odoo2 = odoorpc.ODOO('destiny_server', port=8069)
odoo.login('source_db_name', 'source_user', 'source_password')
odoo2.login('destiny_db_name', 'destiny_user', 'destiny_password')
mrp_obj = odoo.env['mrp.bom']
mrp_ids = mrp_obj.search([])
mrps = mrp_obj.browse(mrp_ids)
logging.basicConfig(filename="mrp.log", level=logging.DEBUG)
count = 0
with progressbar.ProgressBar(max_value=len(mrps)) as bar:
    for bom in mrps:
        count += 1
        bar.update(count)
        product_tmpl_id = odoo2.env['product.template'].search(
            [('name', '=', bom.product_tmpl_id.name)])
        uom_id = odoo2.env['product.uom'].search(
            [('name', '=', bom.product_uom.name)])
        company_id = odoo2.env['res.company'].search(
            [('name', '=', bom.company_id.name)])
        lines = []
        for kit in bom.bom_line_ids:
            product_product_id = odoo2.env['product.product'].search(
                [('name', '=', kit.product_id.name)])
            product_uom_id = odoo2.env['product.uom'].search(
                [('name', '=', kit.product_uom.name)])
            line = (0, 0, {
                'product_id': (
                    product_product_id[0] if product_product_id else False),
                'product_qty': kit.product_qty,
                'uom_id': product_uom_id[0] if product_uom_id else False
                })
            lines.append(line)
        try:
            odoo2.execute('mrp.bom', 'create', {
                'product_tmpl_id': (
                    product_tmpl_id[0] if product_tmpl_id else False),
                'product_qty': bom.product_qty,
                'product_uom_id': uom_id[0] if uom_id else False,
                'code': bom.code,
                'type': bom.type,
                'company_id': company_id[0] if company_id else False,
                'born_line_ids': [x for x in lines],
                'position': bom.position,
                'sequence': bom.sequence,
                'active': bom.active,
                'date_start': bom.date_start,
                'date_stop': bom.date_stop,
                'product_rounding': bom.product_rounding,
                'product_efficiency': bom.product_efficiency
                })
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            l = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            print '*' * 20 + str(
                bom.product.tmpl_id[0] if bom.product_tmpl_id else False)
            logging.debug(l)
            logging.debug("\n")
