# -*- coding: utf-8 -*-
import odoorpc
import progressbar
import logging
import sys
import traceback
odoo = odoorpc.ODOO('localhost', port=8069)
odoo2 = odoorpc.ODOO('localhost', port=8069)
odoo.login(
    'local_source_db_name',
    'local_source_username',
    'local_source_password')
odoo2.login(
    'local_destiny_db_name',
    'local_destiny_username',
    'local_destiny_password')
partner_obj = odoo.env['res.partner']
partner_ids = partner_obj.search([])
partners = partner_obj.browse(partner_ids)
logging.basicConfig(filename="partner.log", level=logging.DEBUG)
count = 0
w_parent = []
c_parent = []

with progressbar.ProgressBar(max_value=len(partners)) as bar:
    print "**** Guardando partners absolutos y relativos ****"
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
        # regimen_id = odoo2.env['cfd_mx.regimen'].search(
        #    [('name', '=', rec.regimen_id.name)])
        # property_purchase_currency_id = odoo2.env['res.currency'].search(
        #    [('name', '=', rec.property_purchase_currency_id.name)])
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
        # metodo_pago = odoo2.env['cfd_payment.formapago'].search(
        #    [('name', '=', rec.metodo_pago.name)])
        property_account_receivable_id = (
            odoo2.env['account.account'].search(
                [('name', '=', rec.property_account_receivable_id.name)]))
        property_account_payable_id = (
            odoo2.env['account.account'].search(
                [('name', '=', rec.property_account_payable_id.name)]))
        record_exist = odoo2.env['res.partner'].search(
            [('name', '=', rec.name)])
        try:
            if not record_exist:
                odoo2.execute('res.partner', 'create', {
                    'name': rec.name,
                    'street': rec.street,
                    # 'noExterior': rec.noExterior,
                    # 'noInterior': rec.noInterior,
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
                    # 'regimen_id': (
                    #     regimen_id[0] if len(regimen_id) > 0 else False),
                    'comment': rec.comment,
                    'customer': rec.customer,
                    'supplier': rec.supplier,
                    # 'property_purchase_currency_id': (
                    #    property_purchase_currency_id[0] if len(
                    #        property_purchase_currency_id) > 0 else False),
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
                    # 'metodo_pago': (
                    #    metodo_pago[0] if len(metodo_pago) > 0 else False),
                    # 'vat': rec.vat,
                    # 'supplier_type': rec.supplier_type,
                    # 'operation_type': rec.operation_type,
                    # 'fiscal_id': rec.fiscal_id,
                    'property_account_receivable_id': (
                        property_account_receivable_id[0] if len(
                            property_account_receivable_id) > 0 else False),
                    'property_account_payable_id': (
                        property_account_payable_id[0] if len(
                            property_account_payable_id) > 0 else False)
                    })
            else:
                print("Ya existe el partner " + rec.name + " por lo tanto"
                      " no sera creado:")
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
        # regimen_id = odoo2.env['cfd_mx.regimen'].search(
        #    [('name', '=', record.regimen_id.name)])
        # property_purchase_currency_id = odoo2.env['res.currency'].search(
        #     [('name', '=', record.property_purchase_currency_id.name)])
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
        # metodo_pago = odoo2.env['cfd_payment.formapago'].search(
        #    [('name', '=', record.metodo_pago.name)])
        property_account_receivable_id = (
            odoo2.env['account.account'].search(
                [('name', '=', record.property_account_receivable_id.name)]))
        property_account_payable_id = (
            odoo2.env['account.account'].search(
                [('name', '=', record.property_account_payable_id.name)]))
        parent_id = (odoo2.env['res.partner'].search(
            [('name', '=', record.parent_id.name)]))
        record_exist = odoo2.env['res.partner'].search(
            [('name', '=', record.name)])
        try:
            if not record_exist:
                odoo2.execute('res.partner', 'create', {
                    'name': record.name,
                    'street': record.street,
                    # 'noExterior': record.noExterior,
                    # 'noInterior': record.noInterior,
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
                    # 'regimen_id': (
                    #    regimen_id[0] if len(regimen_id) > 0 else False),
                    'comment': record.comment,
                    'customer': record.customer,
                    'supplier': record.supplier,
                    # 'property_purchase_currency_id': (
                    #    property_purchase_currency_id[0] if len(
                    #        property_purchase_currency_id) > 0 else False),
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
                    # 'metodo_pago': (
                    #   metodo_pago[0] if len(metodo_pago) > 0 else False),
                    # 'vat': record.vat,
                    # 'supplier_type': record.supplier_type,
                    # 'operation_type': record.operation_type,
                    # 'fiscal_id': record.fiscal_id,
                    'property_account_receivable_id': (
                        property_account_receivable_id[0] if len(
                            property_account_receivable_id) > 0 else False),
                    'property_account_payable_id': (
                        property_account_payable_id[0] if len(
                            property_account_payable_id) > 0 else False),
                    'parent_id': (
                        parent_id[0] if len(parent_id) > 0 else False)
                    })
            else:
                print("Ya existe el partner " + record.name + " por lo tanto"
                      " no sera creado: " + "\n")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            print '*' * 20 + record.name
            logging.debug(lines)
