#!/usr/bin/env python
# -*- coding: utf-8 -*-

import odoorpc
import progressbar
import logging
import sys
import traceback
odoo = odoorpc.ODOO('source_server', port=8069)
odoo2 = odoorpc.ODOO('destiny_server', port=8069)
odoo.login('source_db_name', 'source_user', 'source_password')
odoo2.login('destiny_db_name', 'destiny_user', 'destiny_password')

cuenta_obj = odoo.env['account.account']
cuenta_ids = cuenta_obj.search([])
cuentas = cuenta_obj.browse(cuenta_ids)
logging.basicConfig(filename="cuenta.log", level=logging.DEBUG)
count = 0
count_exist = 0
with progressbar.ProgressBar(max_value=len(cuentas)) as bar:
    for cuenta in cuentas:
        count += 1
        bar.update(count)
        taxes = []
        for tax in cuenta.tax_ids:
            tax_id = odoo2.env['account.tax'].search(
                [('name', '=', tax.name)])
            taxes.append(tax_id[0])
        tags = []
        for tag in cuenta.tag_ids:
            tag_id = odoo2.env['account.account.tag'].search(
                [('name', '=', tag.name)])
            tags.append(tag_id[0])
        currency_id = odoo2.env['res.currency'].search(
            [('name', '=', cuenta.currency_id.name)])
        user_type_id = odoo2.env['account.account.type'].search(
            [('name', '=', cuenta.user_type_id.name)])
        account = odoo2.env['account.account'].search(
            [('name', '=', cuenta.name), ('code', '=', cuenta.code)])
        try:
            if not account:
                odoo2.execute('account.account', 'create', {
                    'code': cuenta.code,
                    'name': cuenta.name,
                    'user_type_id': (
                        user_type_id[0] if len(user_type_id) > 0 else False),
                    'tax_ids': ([(6, 0, taxes)] if taxes else False),
                    'tag_ids': ([(6, 0, tags)] if tags else False),
                    'currency_id': (
                        currency_id[0] if len(currency_id) > 0 else False),
                    'reconcile': cuenta.reconcile,
                    'deprecated': cuenta.deprecated
                })
            else:
                print("Ya existe la cuenta: " + cuenta.name + " por lo tanto"
                      " no sera creada:")
                count_exist += 1
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            print cuenta.name
            logging.debug(lines)
    print ("Cuentas que ya existian: " + str(count_exist))
