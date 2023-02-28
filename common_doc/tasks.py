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
from frappe.utils import (
	add_days,
	add_months,
	cint,
	date_diff,
	flt,
	get_datetime,
	get_last_day,
	getdate,
	month_diff,
	nowdate,
	today,
	get_normalized_weekday_index,
	)

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
	today = datetime.today()
	# print("Background job Exchange Rate is started")

	ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange Rate',
		'date': add_days(today,1),
		'to_currency': 'KRW'
	})
	
	if not ex_exists:
		common_doc.common_doc.doctype.currency_exchange_rate.api.get_exchange_rate_all(exchange_date=today.strftime('%Y-%m-%d'))
		# common_doc.tasks.cron

def cron_ca():
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	today = datetime.today()
	yesterday = datetime.today() - timedelta(1)
	# print("Background job Exchange Rate is started")


	caex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange',
		'date': yesterday.strftime('%Y-%m-%d'),
		'to_currency': 'CAD'
	})
	if not caex_exists:
		common_doc.common_doc.doctype.currency_exchange_rate.api.import_canada_exchange_rate(exchange_date=yesterday.strftime('%Y-%m-%d'))
def cron_us():
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	today = datetime.today()
	# print("Background job Exchange Rate is started")
	ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange Rate',
		'date': add_days(today,1),
		'to_currency': 'KRW'
	})
	if not ex_exists:
		common_doc.common_doc.doctype.currency_exchange_rate.api.get_exchange_rate_all(exchange_date=add_days(today,1))
	
	mx_ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange',
		'date': today.strftime('%Y-%m-%d'),
		'to_currency': 'MXN'
	})
	if not mx_ex_exists:
		common_doc.common_doc.doctype.currency_exchange_rate.api.create_mx_exchange()
		# common_doc.tasks.cron