import odoorpc
import progressbar
import logging
import sys
import traceback

logging.basicConfig(filename="account_invoice.log", level=logging.DEBUG)
odoo = odoorpc.ODOO('source_server', port=8069)
odoo2 = odoorpc.ODOO('destiny_server', port=8069)
odoo.login('source_db_name', 'source_user', 'source_password')
odoo2.login('destiny_db_name', 'destiny_user', 'destiny_password')
invoice_obj = odoo.env['account.invoice']
invoice_ids = invoice_obj.search([])
invoices = invoice_obj.browse(invoice_ids)

count = 0
with progressbar.ProgressBar(max_value=len(invoices)) as bar:
    for invoice in invoices:
        count += 1
        bar.update(count)
        partner_id = odoo2.env['res.partner'].search(
            [('name', '=', invoice.partner_id.name)])
        payment_term_id = odoo2.env['account.payment.term'].search(
            [('name', '=', invoice.payment_term_id.name)])
        user_id = odoo2.env['res.users'].search(
            [('name', '=', invoice.user_id.name)])
        payment_method_id = odoo2.env['oml.payment.method'].search(
            [('name', '=', invoice.payment_method_id.name)])
        account_payment_id = odoo2.env['res.partner.bank'].search(
            [('acc_number', '=', invoice.account_payment_id.acc_number)])
        journal_id = odoo2.env['account.journal'].search(
            [('name', '=', invoice.journal_id.name)])
        account_id = odoo2.env['account.account'].search(
            [('name', '=', invoice.account_id.name)])
        address_issued_id = odoo2.env['res.partner'].search(
            [('name', '=', invoice.address_issued_id.name)])
        fiscal_position_id = odoo2.env['account.fiscal.position'].search(
            [('name', '=', invoice.fiscal_position_id.name)])
        invoice_line_ids = []

        for invoice_line in invoice.invoice_line_ids:
            product_id = odoo2.env['product.product'].search(
                [('name', '=', invoice_line.product_id.name)])
            account_id = odoo2.env['account.account'].search(
                [('name', '=', invoice_line.account_id.name)])
            invoice_tax = []

            for invoice_line_tax in invoice_line.invoice_line_tax_ids:
                tax = odoo2.env['account.tax'].search(
                    [('name', '=', invoice_line_tax.name)])
                invoice_tax.append(tax[0])
            line = (0, 0, {
                'product_id': product_id[0],
                'name': invoice_line.name,
                'quantity': invoice_line.quantity,
                'price_unit': invoice_line.price_unit,
                'invoice_line_tax_ids': [(6, 0, invoice_tax)]
            })
            invoice_line_ids.append(line)
        try:
            odoo2.execute('account.invoice', 'create', {
                'name': invoice.name,
                'type': invoice.type,
                'partner_id': partner_id[0],
                'date_invoice': invoice.date_invoice,
                'payment_term_id': payment_term_id[0] or False,
                'user_id': user_id[0] or False,
                'payment_method_id': payment_method_id[0] or False,
                'account_payment_id': account_payment_id[0] or False,
                'journal_id': journal_id[0],
                'account_id': account_id[0],
                'date_due': invoice.date_due,
                'payment_police': invoice.payment_police,
                'address_issued_id': address_issued_id[0] or False,
                'fiscal_position_id': fiscal_position_id[0] or False,
                'invoice_line_ids': [x for x in invoice_line_ids],
                # 'tax_line_ids': [x for x in tax_line_ids],
                })
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            print '*' * 20 + invoice.id
            logging.debug(lines)
