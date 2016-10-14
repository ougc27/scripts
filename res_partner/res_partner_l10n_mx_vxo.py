import odoorpc
import progressbar
import logging
import sys
import traceback
odoo = odoorpc.ODOO('source_server', port=8069)
odoo2 = odoorpc.ODOO('destiny_server', port=8069)
odoo.login('source_db_name', 'source_user', 'source_password')
odoo2.login('destiny_db_name', 'destiny_user', 'destiny_password')
partner_obj = odoo.env['res.partner']
partner_ids = partner_obj.search([])
partners = partner_obj.browse(partner_ids)
logging.basicConfig(filename="partner.log", level=logging.DEBUG)
count = 0
w_parent = []
c_parent = []
with progressbar.ProgressBar(max_value=len(partners)) as bar:
    print "**** Calculando y separando los partners absolutos y relativos ****"
    for partner in partners:
        count += 1
        bar.update(count)
        try:
            if not partner.parent_id:
                w_parent.append(partner)
            else:
                c_parent.append(partner)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            print '*' * 20 + partner.name
            logging.debug(lines)
    print '**** Partners Abosultos: ' + str(len(w_parent))
    print '**** Partners Relativos: ' + str(len(c_parent))
    count = 0
with progressbar.ProgressBar(max_value=len(w_parent)) as bar:
    print "**** Creando Partners Absoulutos ****"
    for rec in w_parent:
        count += 1
        bar.update(count)
        state_id = odoo2.env['res.country.state'].search(
            [('name', '=', rec.state_id.name)])
        country_id = odoo2.env['res.country'].search(
            [('name', '=', rec.country_id.name)])
        regimen_fiscal_id = odoo2.env['regimen.fiscal'].search(
            [('name', '=', rec.regimen_fiscal_id.name)])
        property_purchase_currency_id = odoo2.env['res.currency'].search(
            [('name', '=', rec.property_purchase_currency_id.name)])
        property_product_pricelist = odoo2.env['product.pricelist'].search(
            [('name', '=', rec.property_product_pricelist.name)])
        property_stock_customer = odoo2.env['stock.location'].search(
            [('name', '=', rec.property_stock_customer.name)])
        property_stock_supplier = odoo2.env['stock.location'].search(
            [('name', '=', rec.property_stock_supplier.name)])
        property_payment_term_id = odoo2.env['account.payment.term'].search(
            [('name', '=', rec.property_stock_customer.name)])
        property_supplier_payment_term_id = (
            odoo2.env['account.payment.term'].search(
                [('name', '=', rec.property_stock_customer.name)]))
        property_account_position_id = (
            odoo2.env['account.fiscal.position'].search(
                [('name', '=', rec.property_account_position_id.name)]))
        payment_method_id = odoo2.env['oml.payment.method'].search(
            [('name', '=', rec.payment_method_id.name)])
        property_account_receivable_id = (
            odoo2.env['account.account'].search(
                [('name', '=', rec.property_account_receivable_id.name)]))
        property_account_payable_id = (
            odoo2.env['account.account'].search(
                [('name', '=', rec.property_account_payable_id.name)]))
        try:
            odoo2.execute('res.partner', 'create', {
                'name': rec.name,
                'street': rec.street,
                'l10n_mx_street3': rec.l10n_mx_street3,
                'l10n_mx_street4': rec.l10n_mx_street4,
                'street2': rec.street2,
                'city': rec.city,
                'state_id': (state_id[0] if len(state_id) > 0 else False),
                'zip': rec.zip,
                'country_id': (
                    country_id[0] if len(country_id) > 0 else False),
                'website': rec.website,
                'phone': rec.phone,
                'mobile': rec.mobile,
                'fax': rec.fax,
                'email': rec.email,
                'regimen_fiscal_id': (
                    regimen_fiscal_id[0] if len(
                        regimen_fiscal_id) > 0 else False),
                'comment': rec.comment,
                'customer': rec.customer,
                'supplier': rec.supplier,
                'property_purchase_currency_id': (
                    property_purchase_currency_id[0] if len(
                        property_purchase_currency_id) > 0 else False),
                'notify_email': rec.notify_email,
                'opt_out': rec.opt_out,
                'property_product_pricelist': (
                    property_product_pricelist[0] if len(
                        property_product_pricelist) > 0 else False),
                'ref': rec.ref,
                'property_stock_customer': (
                    property_stock_customer[0] if len(
                        property_stock_customer) > 0 else False),
                'property_stock_supplier': (
                    property_stock_supplier[0] if len(
                        property_stock_supplier) > 0 else False),
                'property_payment_term_id': (
                    property_payment_term_id[0] if len(
                        property_payment_term_id) > 0 else False),
                'property_supplier_payment_term_id': (
                    property_supplier_payment_term_id[0] if len(
                        property_supplier_payment_term_id) > 0 else False),
                'property_account_position_id': (
                    property_account_position_id[0] if len(
                        property_account_position_id) > 0 else False),
                'payment_method_id': (
                    payment_method_id[0] if len(
                        payment_method_id) > 0 else False),
                'property_account_receivable_id': (
                    property_account_receivable_id[0] if len(
                        property_account_receivable_id) > 0 else False),
                'property_account_payable_id': (
                    property_account_payable_id[0] if len(
                        property_account_payable_id) > 0 else False)
                })
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            print '*' * 20 + rec.name
            logging.debug(lines)
            logging.debug("\n")
    count = 0
with progressbar.ProgressBar(max_value=len(c_parent)) as bar:
    print "**** Creando Partners Relativos ****"
    for record in c_parent:
        count += 1
        bar.update(count)
        state_id = odoo2.env['res.country.state'].search(
            [('name', '=', record.state_id.name)])
        country_id = odoo2.env['res.country'].search(
            [('name', '=', record.country_id.name)])
        regimen_fiscal_id = odoo2.env['regimen.fiscal'].search(
            [('name', '=', record.regimen_fiscal_id.name)])
        property_purchase_currency_id = odoo2.env['res.currency'].search(
            [('name', '=', record.property_purchase_currency_id.name)])
        property_product_pricelist = odoo2.env['product.pricelist'].search(
            [('name', '=', record.property_product_pricelist.name)])
        property_stock_customer = odoo2.env['stock.location'].search(
            [('name', '=', record.property_stock_customer.name)])
        property_stock_supplier = odoo2.env['stock.location'].search(
            [('name', '=', record.property_stock_supplier.name)])
        property_payment_term_id = odoo2.env['account.payment.term'].search(
            [('name', '=', record.property_stock_customer.name)])
        property_supplier_payment_term_id = (
            odoo2.env['account.payment.term'].search(
                [('name', '=', record.property_stock_customer.name)]))
        property_account_position_id = (
            odoo2.env['account.fiscal.position'].search(
                [('name', '=', record.property_account_position_id.name)]))
        payment_method_id = odoo2.env['oml.payment.method'].search(
            [('name', '=', record.payment_method_id.name)])
        property_account_receivable_id = (
            odoo2.env['account.account'].search(
                [('name', '=', record.property_account_receivable_id.name)]))
        property_account_payable_id = (
            odoo2.env['account.account'].search(
                [('name', '=', record.property_account_payable_id.name)]))
        parent_id = (odoo2.env['res.partner'].search(
            [('name', '=', record.parent_id.name)]))
        try:
            odoo2.execute('res.partner', 'create', {
                'name': record.name,
                'street': record.street,
                'l10n_mx_street3': record.l10n_mx_street3,
                'l10n_mx_street4': record.l10n_mx_street4,
                'street2': record.street2,
                'city': record.city,
                'state_id': (state_id[0] if len(state_id) > 0 else False),
                'zip': record.zip,
                'country_id': (
                    country_id[0] if len(country_id) > 0 else False),
                'website': record.website,
                'phone': record.phone,
                'mobile': record.mobile,
                'fax': record.fax,
                'email': record.email,
                'regimen_fiscal_id': (
                    regimen_fiscal_id[0] if len(
                        regimen_fiscal_id) > 0 else False),
                'comment': record.comment,
                'customer': record.customer,
                'supplier': record.supplier,
                'property_purchase_currency_id': (
                    property_purchase_currency_id[0] if len(
                        property_purchase_currency_id) > 0 else False),
                'notify_email': record.notify_email,
                'opt_out': record.opt_out,
                'property_product_pricelist': (
                    property_product_pricelist[0] if len(
                        property_product_pricelist) > 0 else False),
                'ref': record.ref,
                'property_stock_customer': (
                    property_stock_customer[0] if len(
                        property_stock_customer) > 0 else False),
                'property_stock_supplier': (
                    property_stock_supplier[0] if len(
                        property_stock_supplier) > 0 else False),
                'property_payment_term_id': (
                    property_payment_term_id[0] if len(
                        property_payment_term_id) > 0 else False),
                'property_supplier_payment_term_id': (
                    property_supplier_payment_term_id[0] if len(
                        property_supplier_payment_term_id) > 0 else False),
                'property_account_position_id': (
                    property_account_position_id[0] if len(
                        property_account_position_id) > 0 else False),
                'payment_method_id': (
                    payment_method_id[0] if len(
                        payment_method_id) > 0 else False),
                'property_account_receivable_id': (
                    property_account_receivable_id[0] if len(
                        property_account_receivable_id) > 0 else False),
                'property_account_payable_id': (
                    property_account_payable_id[0] if len(
                        property_account_payable_id) > 0 else False),
                'parent_id': (
                    parent_id[0] if len(parent_id) > 0 else False)
                })

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            print '*' * 20 + record.name
            logging.debug(lines)
