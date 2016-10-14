import odoorpc
import progressbar
import logging
odoo = odoorpc.ODOO('source_server', port=8069)
odoo2 = odoorpc.ODOO('destiny_server', port=8069)
odoo.login('source_db_name', 'source_user', 'source_password')
odoo2.login('destiny_db_name', 'destiny_user', 'destiny_password')
odoo2.login('Jarsa', 'admin', '177345')
partner_obj = odoo.env['res.partner']
partner_ids = partner_obj.search([])
partners = partner_obj.browse(partner_ids)
logging.basicConfig(filename="test.log", level=logging.DEBUG)
count = 0
with progressbar.ProgressBar(max_value=len(partners)) as bar:
    for rec in partners:
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
        record_exist = odoo2.env['res.partner'].search(
            [('name', '=', rec.name)])
        import ipdb; ipdb.set_trace()
        dictio = {
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
                    property_account_payable_id) > 0 else False)}
