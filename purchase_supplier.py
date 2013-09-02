# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) Javier Duran
#                  Mariano Ruiz (Enterprise Objects Consulting)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from osv import fields
from osv import osv

class product_product(osv.osv):
	_name = 'product.product'
	_inherit = 'product.product'
	
	def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
		ids=[]
		if not args:
			args=[]
		if not context:
			context={}
		if context and context.has_key('partner_id') and context['partner_id']:
			# Warn: ps.name is the pk of the partner in the product_supplierinfo model
			cr.execute('SELECT p.id ' \
					'FROM product_product AS p ' \
					'INNER JOIN product_template AS t ' \
					'ON p.product_tmpl_id=t.id ' \
					'INNER JOIN product_supplierinfo AS ps ' \
					'ON ps.product_id=t.id ' \
					'WHERE ps.name = %s ' \
					'AND ps.product_code = %s ' \
					'AND t.purchase_ok = True ' \
					'AND p.active = True ' \
					'ORDER BY p.id',
					(context['partner_id'],name))
			res = cr.fetchall()
			ids = map(lambda x:x[0], res)
			if not len(ids):
				cr.execute('SELECT p.id ' \
					'FROM product_product AS p ' \
					'INNER JOIN product_template AS t ' \
					'ON p.product_tmpl_id=t.id ' \
					'INNER JOIN product_supplierinfo AS ps ' \
					'ON ps.product_id=t.id ' \
					'WHERE ps.name = %s ' \
					'AND ps.product_name = %s ' \
					'AND t.purchase_ok = True ' \
                                        'AND p.active = True ' \
					'ORDER BY p.id',
					(context['partner_id'],name ))
				res = cr.fetchall()
				ids = map(lambda x:x[0], res)
			if not len(ids):
				cr.execute('SELECT p.id ' \
					'FROM product_product AS p ' \
					'INNER JOIN product_template AS t ' \
					'ON p.product_tmpl_id=t.id ' \
					'INNER JOIN product_supplierinfo AS ps ' \
					'ON ps.product_id=t.id ' \
					'WHERE ps.name = %s ' \
					'AND p.ean13 = %s ' \
					'AND t.purchase_ok = True ' \
				        'AND p.active = True ' \
					'ORDER BY p.id',
					(context['partner_id'],name ))
				res = cr.fetchall()
				ids = map(lambda x:x[0], res)
			if not len(ids):
				if operator in ('like', 'ilike'):
					name='%'+name+'%'
				cr.execute('SELECT p.id ' \
					'FROM product_product AS p ' \
					'INNER JOIN product_template AS t ' \
					'ON p.product_tmpl_id=t.id ' \
					'INNER JOIN product_supplierinfo AS ps ' \
					'ON ps.product_id=t.id ' \
					'WHERE ps.name = %s ' \
					'AND ps.product_code '+operator+' %s ' \
					'AND t.purchase_ok = True ' \
					'AND p.active = True ' \
					'ORDER BY p.id',
					(context['partner_id'],name ))
				res = cr.fetchall()
				ids = map(lambda x:x[0], res)
				ids = set(ids)
				cr.execute('SELECT p.id ' \
					'FROM product_product AS p ' \
					'INNER JOIN product_template AS t ' \
					'ON p.product_tmpl_id=t.id ' \
					'INNER JOIN product_supplierinfo AS ps ' \
					'ON ps.product_id=t.id ' \
					'WHERE ps.name = %s ' \
					'AND ps.product_name '+operator+' %s ' \
					'AND t.purchase_ok = True ' \
					'AND p.active = True ' \
					'ORDER BY p.id',
					(context['partner_id'],name ))
				res = cr.fetchall()
				ids.update(map(lambda x:x[0], res))
			if not len(ids):
				if operator in ('like', 'ilike'):
					name='%'+name+'%'
				cr.execute('SELECT p.id ' \
					'FROM product_product AS p ' \
					'INNER JOIN product_template AS t ' \
					'ON p.product_tmpl_id=t.id ' \
					'INNER JOIN product_supplierinfo AS ps ' \
					'ON ps.product_id=t.id ' \
					'WHERE ps.name = %s ' \
					'AND p.default_code '+operator+' %s ' \
					'AND t.purchase_ok = True ' \
					'AND p.active = True ' \
					'ORDER BY p.id',
					(context['partner_id'],name ))
				res = cr.fetchall()
				ids = map(lambda x:x[0], res)
				ids = set(ids)
				cr.execute('SELECT p.id ' \
					'FROM product_product AS p ' \
					'INNER JOIN product_template AS t ' \
					'ON p.product_tmpl_id=t.id ' \
					'INNER JOIN product_supplierinfo AS ps ' \
					'ON ps.product_id=t.id ' \
					'WHERE ps.name = %s ' \
					'AND t.name '+operator+' %s ' \
					'AND t.purchase_ok = True ' \
					'AND p.active = True ' \
					'ORDER BY p.id',
					(context['partner_id'],name ))
				res = cr.fetchall()
				ids.update(map(lambda x:x[0], res))
		if isinstance(ids, set):
			ids = list(ids)
		ids = list(ids)
		if not len(ids):
			ids = self.search(cr, user, [('default_code','=',name)]+ args, limit=limit, context=context)
		if not len(ids):
			ids = self.search(cr, user, [('ean13','=',name)]+ args, limit=limit, context=context)
		if not len(ids):
			ids = self.search(cr, user, [('default_code',operator,name)]+ args, limit=limit, context=context)
			ids += self.search(cr, user, [('name',operator,name)]+ args, limit=limit, context=context)
			ids = list(set(ids))
		result = self.name_get(cr, user, ids, context)
		return result

product_product()
