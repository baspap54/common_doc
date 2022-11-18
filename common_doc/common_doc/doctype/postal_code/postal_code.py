# Copyright (c) 2022, John and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class PostalCode(Document):
	def before_insert(self):
		self.location = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":['+str(self.longitude) +','+str(self.latitude) +']}}]}'

