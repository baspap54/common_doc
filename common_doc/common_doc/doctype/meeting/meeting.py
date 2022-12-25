# Copyright (c) 2022, John and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Meeting(Document):
	def validate(self):
		""""Missing Name"""
		for attendee in self.attendees:
			if not attendee.full_name:
				attendee.full_name = self.get_full_name(attendee.attendee)

	def get_full_name(attendee):
		user = frappe.get_doc("User", attendee)
		return " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))