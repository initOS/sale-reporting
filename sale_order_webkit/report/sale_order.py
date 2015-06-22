# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Nicolas Bessi, Vincent Renaville, Guewen Baconnier
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp.addons.report_webkit.webkit_report import webkit_report_extender

@webkit_report_extender("sale.report_sale_order")
def extend_sale_report_webkit(pool, cr, uid, localcontext, context):
    res_users_obj = pool['res.users']
    model_data_obj = pool['ir.model.data']

    company_vat = res_users_obj.browse(cr, uid, uid, context=context)\
        .company_id.partner_id.vat

    def show_discount(user_id):
        try:
            group_id = model_data_obj.get_object_reference(
                cr,
                uid,
                'sale',
                'group_discount_per_so_line')[1]
            groups = res_users_obj.browse(cr, uid, user_id, context=context).groups_id
            return any(x for x in groups if x.id == group_id)
        except ValueError:
            # group named group_discount_per_so_line doesn't exist
            return False

    localcontext.update({
        'time': time,
        'company_vat': company_vat,
        'show_discount': show_discount,
    })
