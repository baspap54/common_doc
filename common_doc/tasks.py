from __future__ import unicode_literals

import locale
import frappe
import random
import string
import requests
import common_doc.common_doc.doctype.currency_exchange_rate.api
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def all():
	pass
	# print("Scheduler started")
	# letters = string.ascii_letters
	# note = " ".join(random.choice(letters) for i in range(20))
	# new_note = frappe.get_doc( {"doctype":"Note",
	# 						"title":note
	# 						}
	# )
	# new_note.insert()
	# frappe.db.commit()

def daily():
	pass

def hourly():
	pass

def weekly():
	pass

def monthly():
	pass

def cron():
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	x = datetime.now()

	date = str(x)
	# print("Background job Exchange Rate is started")

	ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange Rate',
		'date': date,
		'to_currency': 'KRW'
	})
	
	if not ex_exists:
		common_doc.common_doc.doctype.currency_exchange_rate.api.get_exchange_rate_all(exchange_date=date)
		# common_doc.tasks.cron
		