# Copyright (c) 2021, John and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class PortCode(Document):
	def before_save(self):
		self.country_code = self.country_code.upper()
		self.port_code = self.port_code.upper()
		self.name = self.country_code.upper()+self.port_code.upper()
