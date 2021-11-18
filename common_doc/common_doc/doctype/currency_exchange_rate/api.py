from __future__ import unicode_literals

import locale
import frappe
import random
import string
import requests
import json
from bs4 import BeautifulSoup

def random_string(string_length=8):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(string_length))

@frappe.whitelist()
def get_exchange_rate(**args):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	exchange_date = args.get('exchange_date')
	from_currency = args.get('from_currency')
	to_currency = args.get('to_currency')
	currency_exchange_rate_type = args.get('currency_exchange_rate_type')

	yyyymmdd = exchange_date[0:10]
	print(yyyymmdd)
	yyyy = exchange_date[0:4]
	mm = exchange_date[5:7]
	dd = exchange_date[8:10]
	print(yyyy + mm + dd)


	url1 = 'https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do'
	data = {
		'ajax': 'true',
		'curCd': from_currency,
		'tmpInqStrDt': yyyymmdd,
		'pbldDvCd': '1',
		'pbldSqn': '',
		'inqStrDt': yyyy + mm + dd,
		'inqKindCd': '1',
		'requestTarget': 'searchContentDiv'
	}

	res1 = requests.post(url1, data=data)
	html = res1.content

	soup = BeautifulSoup(html, 'lxml')

#	print(html)
	exchange_rate = 0.0
#	print( ((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip() )
	exyyyy = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[0:4]
	exmm = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[5:7]
	exdd = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[8:10]

	list_td = soup.find_all(name="td", attrs={"class": "txtAr"})
	if currency_exchange_rate_type == 'BASE':
		exchange_rate = list_td[8].text.strip()
	elif currency_exchange_rate_type == 'CAB':
		exchange_rate = list_td[0].text.strip()
	elif currency_exchange_rate_type == 'CAS':
		exchange_rate = list_td[2].text.strip()
	elif currency_exchange_rate_type == 'TTS':
		exchange_rate = list_td[5].text.strip()
	elif currency_exchange_rate_type == 'TTB':
		exchange_rate = list_td[4].text.strip()

	usd_rate = 0.0
	usd_rate = list_td[10].text.strip()


	if locale.atof(exchange_rate) > 0:
		exchange_doc = frappe.new_doc('Currency Exchange Rate')
		exchange_doc.date = exyyyy+"-"+exmm+"-"+exdd
		exchange_doc.from_currency = from_currency
		exchange_doc.to_currency = to_currency
		exchange_doc.usd_rate = locale.atof(usd_rate)
		exchange_doc.rate = locale.atof(exchange_rate)
		if from_currency == "JPY" or from_currency == "VND" or from_currency == "IDR":
			exchange_doc.scale = "1:100"
		else:

			exchange_doc.scale = "1:1"


#		create_exchange_rate(yyyymmdd, currency_cd, exchange_rate)
#	for td_tag in list_td:
#		print(td_tag.text.strip())

#		exchange_rate = td_tag.text.strip()

	print(args)
	print(exchange_doc)
	return exchange_doc

@frappe.whitelist()
def get_exchange_rate_all(**args):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	exchange_date = args.get('exchange_date')
	list_currency = ['USD', 'JPY', 'EUR', 'CNY', 'HKD', 'THB', 'TWD', 'PHP', 'SGD', 'AUD', 'VND', 'GBP', 'CAD', 'MYR',
					 'RUB', 'ZAR', 'NOK', 'NZD', 'DKK', 'MXN', 'MNT', 'BHD', 'BDT', 'BRL', 'BND', 'SAR', 'LKR', 'SEK',
					 'CHF', 'AED', 'DZD', 'OMR', 'JOD', 'ILS', 'EGP', 'INR', 'IDR', 'CZK', 'CLP', 'KZT', 'QAR', 'KES',
					 'COP', 'KWD', 'TZS', 'TRY', 'PKR', 'PLN', 'HUF']

	yyyymmdd = exchange_date[0:10]
	yyyy = exchange_date[0:4]
	mm = exchange_date[5:7]
	dd = exchange_date[8:10]


	for currency_cd in list_currency:
		url1 = 'https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do'
		data = {
			'ajax': 'true',
			'curCd': currency_cd,
			'tmpInqStrDt': yyyymmdd,
			'pbldDvCd': '1',
			'pbldSqn': '',
			'inqStrDt': yyyy + mm + dd,
			'inqKindCd': '1',
			'requestTarget': 'searchContentDiv'
		}
		res1 = requests.post(url1, data=data)
		html = res1.content
		soup = BeautifulSoup(html, 'lxml')
		exchange_rate = 0.0
		list_td = soup.find_all(name="td", attrs={"class": "txtAr"})


		##BASE
		exchange_rate = list_td[8].text.strip()
		##CAB
		exchange_rate_cab = list_td[0].text.strip()
		##CAS
		exchange_rate_cas = list_td[2].text.strip()
		##TTS
		exchange_rate_tts = list_td[5].text.strip()
		##TTB
		exchange_rate_ttb = list_td[4].text.strip()

		usd_rate = 0.0
		usd_rate = list_td[10].text.strip()

		print(((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())
		exyyyy = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[0:4]
		exmm = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[5:7]
		exdd = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[8:10]

		if locale.atof(exchange_rate) > 0:
			create_exchange_rate(exyyyy+"-"+exmm+"-"+exdd, currency_cd, exchange_rate)
			create_currency_exchange_rate('BASE', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate,	usd_rate)
			create_currency_exchange_rate('CAB', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate_cab, usd_rate)
			create_currency_exchange_rate('CAS', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate_cas, usd_rate)
			create_currency_exchange_rate('TTS', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate_tts, usd_rate)
			create_currency_exchange_rate('TTB', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate_ttb, usd_rate)

	print(args)
	return True

@frappe.whitelist()
def get_exchoverseas(**args):
	print("get_exchange_rate_overseas")
	#print(args)
	exchange_date = args.get('exchange_date')
	from_currency = args.get('from_currency')
	to_currency = args.get('to_currency')
	currency_exchange_rate_type = args.get('currency_exchange_rate_type')
	#exchange-rates.abstractapi.com/v1/historical/?api_key=440774db353c4c3abf0602b65e50991c&base=USD&date=2020-08-31
	url = "http://exchange-rates.abstractapi.com/v1/historical/?api_key=440774db353c4c3abf0602b65e50991c&base="+to_currency+"&date="+exchange_date

	resp = requests.get(url)
	#resp = requests.get(url)
	if (resp.status_code == 200):
		res = json.loads(resp.content)
		#print(resp.content)
		#print(resp.json()['exchange_rates'])
		for key, value in resp.json()['exchange_rates'].items():
			#print(key,":",value)
			exchange_doc = frappe.new_doc('Currency Exchange')
			exchange_doc.date = exchange_date
			exchange_doc.from_currency = key
			exchange_doc.to_currency = to_currency
			exchange_doc.rate = value
			exchange_doc.for_buying = 1
			exchange_doc.for_selling = 1
			exchange_doc.insert()
			#print("Exchange rate Created")

		#print(resp.content.get('exchange_rate'))

	#res = requests.get("http://data.fixer.io/api/latest?access_key=0cf7e4582cfe4e7de960de93c6c4bf9a")
	#data = res.json()
	#print(data)

	#print(resp.status_code)
	#if (resp.status_code == 200):
	#	print(resp)
	return True

def create_exchange_rate(curr_date , currency_cd , mrate):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange',
		'date': curr_date,
		'from_currency': currency_cd,
		'to_currency': 'KRW'
	})
	if not ex_exists:
		print("create  " + curr_date + " " + currency_cd + " " + mrate)
		exchange_doc = frappe.new_doc('Currency Exchange')
		exchange_doc.date = curr_date
		exchange_doc.from_currency = currency_cd
		exchange_doc.to_currency = "KRW"
		if currency_cd == "JPY" or currency_cd == "VND" or currency_cd == "IDR":
			exchange_doc.exchange_rate = locale.atof(mrate)/100
		else:
			exchange_doc.exchange_rate = mrate
		exchange_doc.for_buying = 1
		exchange_doc.for_selling = 1
		exchange_doc.insert()

def create_currency_exchange_rate(currency_exchange_rate_type ,curr_date , currency_cd , mrate ,usd_rate):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange Rate',
		'currency_exchange_rate_type': currency_exchange_rate_type,
		'date': curr_date,
		'from_currency': currency_cd,
		'to_currency': 'KRW'
	})
	if not ex_exists:
		print("create  " + curr_date + " " + currency_cd + " " + mrate)
		exchange_doc = frappe.new_doc('Currency Exchange Rate')
		exchange_doc.currency_exchange_rate_type = currency_exchange_rate_type
		exchange_doc.date = curr_date
		exchange_doc.from_currency = currency_cd
		exchange_doc.to_currency = "KRW"
		exchange_doc.rate = mrate
		if currency_cd == "JPY" or currency_cd == "VND" or currency_cd == "IDR":
			exchange_doc.scale = "1:100"
		else:
			exchange_doc.scale = "1:1"
		exchange_doc.usd_rate = usd_rate
		exchange_doc.insert()



