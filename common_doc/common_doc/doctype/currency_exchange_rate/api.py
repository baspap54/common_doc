from __future__ import unicode_literals
from email import header

import locale
import frappe
import random
import string
import requests
import subprocess
import json
import os
from bs4 import BeautifulSoup
# from pyproj import Proj,transform
from datetime import datetime ,timedelta
import time
import requests
import urllib.request
import re
# import pandas as pd

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
	# print(yyyymmdd)
	yyyy = exchange_date[0:4]
	mm = exchange_date[5:7]
	dd = exchange_date[8:10]
	# print(yyyy + mm + dd)


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

	# print(args)
	# print(exchange_doc)
	return exchange_doc

@frappe.whitelist()
def get_exchange_rate_all(**args):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	exchange_date = args.get('exchange_date')
	# print(exchange_date)
	# list_currency = ['USD', 'JPY', 'EUR', 'CNY', 'HKD', 'THB', 'TWD', 'PHP', 'SGD', 'AUD', 'VND', 'GBP', 'CAD', 'MYR',
	# 				 'RUB', 'ZAR', 'NOK', 'NZD', 'DKK', 'MXN', 'MNT', 'BHD', 'BDT', 'BRL', 'BND', 'SAR', 'LKR', 'SEK',
	# 				 'CHF', 'AED', 'DZD', 'OMR', 'JOD', 'ILS', 'EGP', 'INR', 'IDR', 'CZK', 'CLP', 'KZT', 'QAR', 'KES',
	# 				 'COP', 'KWD', 'TZS', 'TRY', 'PKR', 'PLN', 'HUF']

	yyyymmdd = exchange_date[0:10]
	yyyy = exchange_date[0:4]
	mm = exchange_date[5:7]
	dd = exchange_date[8:10]
	#bench execute common_doc.common_doc.doctype.currency_exchange_rate.api.get_exchange_rate_all --kwargs "{'exchange_date':'2022-08-25'}"
	#https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do?ajax=true&curCd=&tmpInqStrDt=2022-08-25&pbldDvCd=1&pbldSqn=&inqStrDt=20220825&inqKindCd=1&requestTarget=searchContentDiv
	# for currency_cd in list_currency:
	if datetime(int(yyyy),int(mm),int(dd),0,0).weekday() <5 :
		url1 = 'https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do'
		data = {
				'ajax': 'true',
				'curCd': '',
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
		# list_td = soup.find_all(name="td", attrs={"class": "txtAr"})
		list_tr = soup.find_all(name='tr')	
		exyyyy = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[0:4]
		exmm = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[5:7]
		exdd = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[8:10]
		currency_cd = ''
		for tr_el in list_tr:
			list_td = tr_el.find_all(name='td', attrs={"class": "txtAr"})
			list_header = tr_el.find_all(name='td', attrs={"class": "tc"})
			if len(list_td)==11:
				
				if list_header[0].get_text().strip()[-3:] != '00)':
					currency_cd = list_header[0].get_text().strip()[-3:] 
				else :
					currency_cd = (list_header[0].get_text().strip()[-9:])[0:3]
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
				# print(exyyyy+exmm+exdd+'---'+ currency_cd + list_td[0].get_text())

				if locale.atof(exchange_rate) > 0:
					create_exchange_rate(exyyyy+"-"+exmm+"-"+exdd, currency_cd,'KRW' ,exchange_rate)
					create_currency_exchange_rate('BASE', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate,	usd_rate)
					create_currency_exchange_rate('CAB', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate_cab, usd_rate)
					create_currency_exchange_rate('CAS', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate_cas, usd_rate)
					create_currency_exchange_rate('TTS', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate_tts, usd_rate)
					create_currency_exchange_rate('TTB', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate_ttb, usd_rate)
		return True

	# 	# print(((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())


		# if locale.atof(exchange_rate) > 0:
		# 	create_exchange_rate(exyyyy+"-"+exmm+"-"+exdd, currency_cd, exchange_rate)
		# 	create_currency_exchange_rate('BASE', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate,	usd_rate)
		# 	create_currency_exchange_rate('CAB', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate_cab, usd_rate)
		# 	create_currency_exchange_rate('CAS', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate_cas, usd_rate)
		# 	create_currency_exchange_rate('TTS', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate_tts, usd_rate)
		# 	create_currency_exchange_rate('TTB', exyyyy + "-" + exmm + "-" + exdd, currency_cd, exchange_rate_ttb, usd_rate)

	# print(args)
# return True

@frappe.whitelist()
def get_calendar(**kwargs):
	# print("get_calendar")
	# print(kwargs)
	cal_year = ""
	country_cd = kwargs.get('country_cd')
	cal_year = kwargs.get('year')
	secrets_file = os.path.join(os.getcwd(), 'secrets.json')
	now = datetime.now()
	yyyy = ""
	if cal_year=="":
		yyyy = now.strftime("%Y")
	else :
		yyyy= cal_year
	# bench execute common_doc.common_doc.doctype.currency_exchange_rate.api.get_calendar --kwargs "{'country_cd':'KR','year':'2022'}"
	#yyyy="2022"
	with open(secrets_file) as f:
		secrets = json.load(f)
	#calendar = "en.south_korea%23holiday%40group.v.calendar.google.com"
	# us_calendar = "6lqpbv8647igscie1ictda2c57nigmcn%40import.calendar.google.com"
	us_calendar ="q5fg70p4b6ob7u9uutc11q24obnba58r@import.calendar.google.com"
	kr_calendar ="qansohiecib58ga9k1bmppvt5oi65b1q@import.calendar.google.com"
	ca_calendar ="9c3j4oiq948vs1pdehn7j7k93ipn0lm9@import.calendar.google.com"
	jp_calendar ="35vbnbma3dqftptpk9l6is0qlo8sbokv@import.calendar.google.com"
	cn_calendar ="bse1jchv6hhvl1vuod9jsndg9b2cl9in@import.calendar.google.com"
	tw_calendar ="2r3ti5fg54f9oehuti8eh08bg2a4uccp@import.calendar.google.com"
	uk_calendar ="gmr65g9mg9r9fiutrmbekhg5iogd14ph@import.calendar.google.com"
	de_calendar ="9997ebqspr9tn8fdeqppcu1iubh1k6t0@import.calendar.google.com"
	fr_calendar ="ubbdc8md7qv9fnocl0seltd4or26c8c4@import.calendar.google.com"
	es_calendar = "t9foe6skmt8akshqb35r9v6j77k68td1@import.calendar.google.com"
	id_calendar = "e5vp7lg6egtbq5nlg72248usu2tbkvc4@import.calendar.google.com"

	calendar = ""
	if country_cd == 'KR':
		calendar = kr_calendar
	elif country_cd == 'US':
		calendar = us_calendar
	elif country_cd == 'CA':
		calendar = ca_calendar
	elif country_cd == 'JP':
		calendar = jp_calendar
	elif country_cd == 'CN':
		calendar = cn_calendar
	elif country_cd == 'TW':
		calendar = tw_calendar
	elif country_cd == 'UK':
		calendar = uk_calendar
	elif country_cd == 'DE':
		calendar = de_calendar
	elif country_cd == 'FR':
		calendar = fr_calendar	
	elif country_cd == 'ES':
		calendar = es_calendar
	elif country_cd == 'ID':
		calendar = id_calendar
	
	# qansohiecib58ga9k1bmppvt5oi65b1q@import.calendar.google.com
	url = "https://www.googleapis.com/calendar/v3/calendars/"+calendar+"/events?key="+secrets["google_api"]+"&orderBy=startTime&singleEvents=true&timeMin="+yyyy+"-01-01T00:00:00Z&timeMax="+yyyy+"-12-31T00:00:00Z"
	# print(url)

	resp = requests.get(url)
	if (resp.status_code == 200):
		res = json.loads(resp.content)
		# company_abbr = frappe.db.get_value('Company', frappe.defaults.get_user_default('Company'), 'abbr')
		# country_cd = frappe.get_system_settings('country') 
		ex_exists = frappe.db.exists('Holiday List',yyyy+country_cd)
		if  ex_exists:
			parent = frappe.get_doc("Holiday List", yyyy+country_cd)
			for holiday in res['items']:
			#print(holiday['summary'])
			#print(holiday['description'])
			#print(holiday['start']['date'])
			#print(json.dumps(holiday['description'],ensure_ascii=False))
			#if '"Public holiday"' == json.dumps(holiday['description'],ensure_ascii=False):
				#print(holiday['summary'])
				#print(holiday['description'])
				#print(holiday['start']['date'])
				holiday_date = json.dumps(holiday['start']['date'],ensure_ascii=False).replace('\"','')
				holiday_name = json.dumps(holiday['summary'],ensure_ascii=False).replace('\"','')
				# print(holiday_date)
				# print(holiday_name)
				
				if frappe.db.exists("Holiday", {"holiday_date": holiday_date}):
					# print("Holiday exists")
					docname = frappe.db.get_value("Holiday", {'holiday_date': holiday_date} ,'name')
					#doc = frappe.get_doc({
					#	'doctype': 'Holiday',
					#	'holiday_date': holiday_date
					#})
					# print(docname+":"+holiday_date)
					frappe.db.set_value("Holiday", docname, "description", holiday_name)
					frappe.db.commit()

					#doc.db_set('description', holiday_name)
					#parent = doc.get_parent()
					#parent.save()

				else:
					parent.append("holidays", {
						'holiday_date': holiday_date,
						'description': holiday_name
					})
					parent.save()
					#frappe.db.commit()
				#child = frappe.new_doc("Holiday")
				#child.update({'holiday_date': holiday_date ,'description': holiday_name ,'parent': parent.name , 'parenttype':'Holiday List' , 'parentfield': 'holidays'})
				#parent.holidays.append(child)
		else:
			cal_doc = frappe.new_doc("Holiday List", yyyy+country_cd)

		#print(res['items']['summary'][1])
		#print(res)
		##for key, value in resp.json()['summary'].items():
		##	print(key)
		##	print(value)

# bench execute common_doc.common_doc.doctype.currency_exchange_rate.api.get_unlocode_port --kwargs "{'country_cd':'us'}"

@frappe.whitelist()
def get_unlocode_port(**kwargs):
	# print(kwargs)
	# proj_UTMK = Proj(init='epsg:5178')
	# proj_WGS84 = Proj(init='epsg:4326')
	country_cd = kwargs.get('country_cd')
	url = 'https://service.unece.org/trade/locode/'+country_cd+'.htm'
	res = requests.get(url)
	html = res.content
	soup = BeautifulSoup(html, 'lxml')
	# list_tr = soup.find_all(name="tr", attrs={"class": "txtAr"})
	
	list_tr = soup.find_all(name="tr")
	# print(len(list_tr))
	for tr_el in list_tr:
		list_td = tr_el.find_all(name='td',attrs={"height": "1","valign":"Top"})
		if len(list_td)==11 and list_td[0].get_text() != 'Ch' and list_td[1].text.strip()[4:7] != '':
			if frappe.db.exists('Port Code',(list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]):
				port_doc = frappe.get_doc('Port Code' ,(list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7])

				port_doc.port_name = list_td[2].get_text()
				port_doc.iata = list_td[8].text.strip()
				port_doc.sub_div = list_td[4].text.strip()
				if list_td[4].text.strip() != '':
					port_doc.title = (list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]+'/'+list_td[2].get_text()+'/'+list_td[4].text.strip()
				else:
					port_doc.title = (list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]+'/'+list_td[2].get_text()

				if list_td[5].get_text()[0:1] == '1':	
					port_doc.sea_port = 1
				else:
					port_doc.sea_port = 0
				
				if list_td[5].get_text()[1:2] == '2':
					port_doc.rail_terminal = 1
				else:
					port_doc.rail_terminal = 0

				if list_td[5].get_text()[2:3] == '3':
					port_doc.road_terminal = 1
				else:
					port_doc.road_terminal = 0

				if list_td[5].get_text()[3:4] == '4':
					port_doc.airport = 1
				else:
					port_doc.airport = 0

				if list_td[5].get_text()[4:5] == '5':
					port_doc.postal_exchange_office = 1
				else:
					port_doc.postal_exchange_office = 0

				if list_td[5].get_text()[5:6] == '6':
					port_doc.mulitmodal_functions = 1
				else:
					port_doc.mulitmodal_functions = 0

				if list_td[5].get_text()[6:7] == '7':
					port_doc.fixed_transport_functions = 1
				else:
					port_doc.fixed_transport_functions = 0

				if list_td[5].get_text()[7:8] == 'B':
					port_doc.border_crossing = 1
				else:
					port_doc.border_crossing = 0

				port_doc.status = list_td[6].get_text()
				port_doc.iata = list_td[8].text.strip()

				if list_td[6].get_text()[0:1] == 'A':
					port_doc.use_yn ='Y'
				else:
					port_doc.use_yn ='N'
				port_doc.description = list_td[10].get_text()
				port_doc.country = frappe.db.get_value('Country',{'code':list_td[1].get_text()[0:2]},'country_name')
				Latitude = 0.000
				Longitude = 0.000
				port_doc.coordinates = list_td[9].text.strip()
				if list_td[9].text.strip() != '':
					# print("["+list_td[9].get_text()+"]") 
					Latitude_minute = int(list_td[9].get_text()[2:4])
					Longitude_minute = int(list_td[9].get_text()[9:11])
					Latitude_degree = int(list_td[9].get_text()[0:2])
					Longitude_degree = int(list_td[9].get_text()[6:9])
					Latitude =  Latitude_degree 
					Longitude = Longitude_degree
					if Latitude_minute >0 :
						Latitude += Latitude_minute/60
					if list_td[9].get_text()[4:5] == 'S':
						Latitude = Latitude *(-1)
					if Longitude_minute >0 :
						Longitude += Longitude_minute/60
					if list_td[9].get_text()[11:12] =='W':
						Longitude = Longitude * (-1)

					port_doc.location = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":['+str(Longitude) +','+str(Latitude) +']}}]}'
				port_doc.latitude = Latitude
				port_doc.longitude = Longitude
				port_doc.save()

			else:
				port_doc = frappe.new_doc('Port Code')
				port_doc.country_code = (list_td[1].get_text())[0:2]
				port_doc.port_code = (list_td[1].get_text())[4:7]
				port_doc.port_name = list_td[2].get_text()
				port_doc.iata = list_td[8].text.strip()
				port_doc.sub_div = list_td[4].text.strip()
				if list_td[4].text.strip() != '':
					port_doc.title = (list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]+'/'+list_td[2].get_text()+'/'+list_td[4].text.strip()
				else:
					port_doc.title = (list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]+'/'+list_td[2].get_text()
				if list_td[5].get_text()[0:1] == '1':	
					port_doc.sea_port = 1
				else:
					port_doc.sea_port = 0
				
				if list_td[5].get_text()[1:2] == '2':
					port_doc.rail_terminal = 1
				else:
					port_doc.rail_terminal = 0

				if list_td[5].get_text()[2:3] == '3':
					port_doc.road_terminal = 1
				else:
					port_doc.road_terminal = 0

				if list_td[5].get_text()[3:4] == '4':
					port_doc.airport = 1
				else:
					port_doc.airport = 0

				if list_td[5].get_text()[4:5] == '5':
					port_doc.postal_exchange_office = 1
				else:
					port_doc.postal_exchange_office = 0

				if list_td[5].get_text()[5:6] == '6':
					port_doc.mulitmodal_functions = 1
				else:
					port_doc.mulitmodal_functions = 0

				if list_td[5].get_text()[6:7] == '7':
					port_doc.fixed_transport_functions = 1
				else:
					port_doc.fixed_transport_functions = 0

				if list_td[5].get_text()[7:8] == 'B':
					port_doc.border_crossing = 1
				else:
					port_doc.border_crossing = 0

				port_doc.status = list_td[6].get_text()
				port_doc.iata = list_td[8].text.strip()

				if list_td[6].get_text()[0:1] == 'A':
					port_doc.use_yn ='Y'
				else:
					port_doc.use_yn ='N'
				port_doc.description = list_td[10].get_text()
				port_doc.country = frappe.db.get_value('Country',{'code':list_td[1].get_text()[0:2]},'country_name')
				Latitude = 0.000
				Longitude = 0.000
				port_doc.coordinates = list_td[9].text.strip()
				if list_td[9].text.strip() != '':
					# print("["+list_td[9].get_text()+"]") 
					Latitude_minute = int(list_td[9].get_text()[2:4])
					Longitude_minute = int(list_td[9].get_text()[9:11])
					Latitude_degree = int(list_td[9].get_text()[0:2])
					Longitude_degree = int(list_td[9].get_text()[6:9])
					Latitude =  Latitude_degree 
					Longitude = Longitude_degree
					if Latitude_minute >0 :
						Latitude += Latitude_minute/60
					if list_td[9].get_text()[4:5] == 'S':
						Latitude = Latitude *(-1)
					if Longitude_minute >0 :
						Longitude += Longitude_minute/60
					if list_td[9].get_text()[11:12] =='W':
						Longitude = Longitude * (-1)

					port_doc.location = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":['+str(Longitude) +','+str(Latitude) +']}}]}'
				port_doc.latitude = Latitude
				port_doc.longitude = Longitude
				

				port_doc.insert(
					ignore_permissions=True, # ignore write permissions during insert
					ignore_links=True, # ignore Link validation in the document
					ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
					ignore_mandatory=True 
				) 
		# for td_el in list_td:
		# 	# print(td_el.get_text())
		# 	print(td_el)

@frappe.whitelist()
def get_exchoverseas(**args):
	# print("get_exchange_rate_overseas")
	#print(args)
	exchange_date = args.get('exchange_date')
	from_currency = args.get('from_currency')
	to_currency = args.get('to_currency')
	secrets_file = os.path.join(os.getcwd(), 'secrets.json')
	with open(secrets_file) as f:
		secrets = json.load(f)
	currency_exchange_rate_type = args.get('currency_exchange_rate_type')
	url = "http://exchange-rates.abstractapi.com/v1/historical/?api_key="+secrets["overseas_exchange_rate"]+"&base="+to_currency+"&date="+exchange_date
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

def create_exchange_rate(curr_date , fr_currency_cd ,to_currency_cd, mrate):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange',
		'date': curr_date,
		'from_currency': fr_currency_cd,
		'to_currency': to_currency_cd
	})
	if not ex_exists:
		# print("create  " + curr_date + " " + currency_cd + " " + mrate)
		exchange_doc = frappe.new_doc('Currency Exchange')
		exchange_doc.date = curr_date
		exchange_doc.from_currency = fr_currency_cd
		exchange_doc.to_currency = to_currency_cd
		exchange_doc.exchange_rate = mrate
		if to_currency_cd == "KRW" :  
			if fr_currency_cd == "JPY" or fr_currency_cd == "VND" or fr_currency_cd == "IDR":
				exchange_doc.exchange_rate = locale.atof(mrate)/100
		exchange_doc.for_buying = 1
		exchange_doc.for_selling = 1
		exchange_doc.insert()

def create_currency_exchange_rate(currency_exchange_rate_type ,curr_date , fr_currency_cd ,to_currency_cd, mrate ,usd_rate):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange Rate',
		'currency_exchange_rate_type': currency_exchange_rate_type,
		'date': curr_date,
		'from_currency': fr_currency_cd,
		'to_currency': to_currency_cd
	})
	if not ex_exists:
		# print("create  " + curr_date + " " + currency_cd + " " + mrate)
		exchange_doc = frappe.new_doc('Currency Exchange Rate')
		exchange_doc.currency_exchange_rate_type = currency_exchange_rate_type
		exchange_doc.date = curr_date
		exchange_doc.from_currency = fr_currency_cd
		exchange_doc.to_currency = to_currency_cd
		exchange_doc.rate = mrate
		exchange_doc.scale = "1:1"

		if to_currency_cd == "KRW" :  
			if fr_currency_cd == "JPY" or fr_currency_cd == "VND" or fr_currency_cd == "IDR" :
				exchange_doc.scale = "1:100"
			else:
				exchange_doc.scale = "1:1"
		exchange_doc.usd_rate = usd_rate
		exchange_doc.insert()

# bench execute common_doc.common_doc.doctype.currency_exchange_rate.api.import_canada_exchange_rate --kwargs "{'exchange_date':'2022-08-25'}"
@frappe.whitelist()
def import_canada_exchange_rate(**kwargs):
	exchange_date = kwargs.get('exchange_date')
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	if not exchange_date:
		x = datetime.now()
		exchange_date = str(x)
	runwget_exchange(exchange_date)
	time.sleep(3)  # File download wait 3 seconds
	read_exchange_rate(exchange_date)
	move_json(exchange_date)

	


	
def read_exchange_rate(date):
	
	file_path = 'ca_exchange_rate/'+date+'.json'
	with open(file_path, 'r') as file :
		data = json.load(file)
		for exchange_data in data['observations'] :
			# print(exchange_data['d'])
			for ex_key in exchange_data.keys():
				if ex_key != 'd':
					# print(ex_key[-6:][0:3]+exchange_data[ex_key]['v'])
					create_exchange_rate(exchange_data['d'], ex_key[-6:][0:3],'CAD' ,exchange_data[ex_key]['v'])

		# print(data)

def runwget():
	# runcmd('pwd', verbose = True)
	runcmd('wget https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json?start_date=2017-01-03', verbose = True)
	runcmd("mv 'json?start_date=2017-01-03' ca_exchange_rate/2017-01-03.json",verbose = True)

def move_json(date):
	runcmd("mv ca_exchange_rate/"+date+".json  ca_exchange_rate/complete/"+date+".json",verbose = True)

def runwget_exchange(date):
	# runcmd('pwd', verbose = True)
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	if not date: 
		x = datetime.now()
		date = str(x)
	runcmd('wget https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json?start_date='+date, verbose = True)
	runcmd("mv 'json?start_date='"+date+ " ca_exchange_rate/"+date+".json",verbose = True)

def runcmd(cmd, verbose = False, *args, **kwargs):
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

def date_loop():
	start = '2020-01-01'
	end = '2020-12-31'
	start_date = datetime.strptime(start,"%Y-%m-%d")
	end_date = datetime.strptime(end,"%Y-%m-%d")
	while start_date <= end_date:
		dates = start_date.strftime("%Y-%m-%d")
		locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
		yyyymmdd = dates[0:10]
		yyyy = dates[0:4]
		mm = dates[5:7]
		dd = dates[8:10]
		#bench execute common_doc.common_doc.doctype.currency_exchange_rate.api.get_exchange_rate_all --kwargs "{'exchange_date':'2022-08-25'}"
		#https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do?ajax=true&curCd=&tmpInqStrDt=2022-08-25&pbldDvCd=1&pbldSqn=&inqStrDt=20220825&inqKindCd=1&requestTarget=searchContentDiv
		# for currency_cd in list_currency:
		if datetime(int(yyyy),int(mm),int(dd),0,0).weekday() <5 :
			print(dates)
			url1 = 'https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do'
			data = {
					'ajax': 'true',
					'curCd': '',
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
			# list_td = soup.find_all(name="td", attrs={"class": "txtAr"})
			list_tr = soup.find_all(name='tr')	
			exyyyy = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[0:4]
			exmm = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[5:7]
			exdd = (((soup.find_all(name="span", attrs={"class": "fl"}))[0].find_all(name="strong")[0]).text.strip())[8:10]
			currency_cd = ''
			for tr_el in list_tr:
				list_td = tr_el.find_all(name='td', attrs={"class": "txtAr"})
				list_header = tr_el.find_all(name='td', attrs={"class": "tc"})
				if len(list_td)==11:
					
					if list_header[0].get_text().strip()[-3:] != '00)':
						currency_cd = list_header[0].get_text().strip()[-3:] 
					else :
						currency_cd = (list_header[0].get_text().strip()[-9:])[0:3]
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
					# print(exyyyy+exmm+exdd+'---'+ currency_cd + list_td[0].get_text())

					if locale.atof(exchange_rate) > 0:
						create_exchange_rate(exyyyy+"-"+exmm+"-"+exdd, currency_cd,'KRW' ,exchange_rate)
						create_currency_exchange_rate('BASE', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate,	usd_rate)
						create_currency_exchange_rate('CAB', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate_cab, usd_rate)
						create_currency_exchange_rate('CAS', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate_cas, usd_rate)
						create_currency_exchange_rate('TTS', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate_tts, usd_rate)
						create_currency_exchange_rate('TTB', exyyyy + "-" + exmm + "-" + exdd, currency_cd, 'KRW' ,exchange_rate_ttb, usd_rate)
		start_date += timedelta(days=1)

@frappe.whitelist()
def get_tax_info(**args):
	print(args)
	bizno=  re.sub("\-", "",  args.get('bizno'))
	dongCode= bizno[3:5]
	country_code = args.get('country_code')
    # docname = args.get('docname')
	x = datetime.now()
	x_str = str(x)
	yyyymmdd = x_str[0:10]
	
	if country_code == "KR" or country_code == "kr":
		# url = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn=false&realScreenId="
		# request = urllib.request.Request(url)
        # #request.add_header("X-Naver-Client-Id", client_id)
		# request.add_header("Accept", "application/xml; charset=UTF-8")
		# request.add_header("Accept-Encoding", "gzip, deflate, br")
		# request.add_header("Accept-Language", "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")
		# request.add_header("Connection", "keep-alive")
		# request.add_header("Content-Length", "257")
		# request.add_header("Content-Type", "application/xml; charset=UTF-8")
		# request.add_header("Host", "teht.hometax.go.kr")
		# request.add_header("Origin", "https://teht.hometax.go.kr")
		# request.add_header("Referer", "https://teht.hometax.go.kr/websquare/websquare.html?w2xPath=/ui/ab/a/a/UTEABAAA13.xml")
		# request.add_header("Sec-Fetch-Mode", "cors")
		# request.add_header("Sec-Fetch-Site", "same-origin")
		# request.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
		# CRLF = "\n"
		# data=""
		# data= "<map id=\"ATTABZAA001R08\">" + CRLF
		# data+=" <pubcUserNo/>" + CRLF
		# data+=" <mobYn>N</mobYn>" + CRLF
		# data+=" <inqrTrgtClCd>1</inqrTrgtClCd>" + CRLF
		# data+=" <txprDscmNo>" + bizno + "</txprDscmNo>" + CRLF
		# data+=" <dongCode>" + dongCode + "</dongCode>" + CRLF
		# data+=" <psbSearch>Y</psbSearch>" + CRLF
		# data+=" <map id=\"userReqInfoVO\"/>" + CRLF
		# data+="</map>" + CRLF
		
		# response = urllib.request.urlopen(request, data=data.encode("utf-8"))
		# rescode = response.getcode()

		secrets_file = os.path.join(os.getcwd(), 'secrets.json')
		with open(secrets_file) as f:
			secrets = json.load(f)
		public_data_bizno_key = secrets["public_data_bizno"]
		url = "https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey="+public_data_bizno_key+"&dataType=JSON"
		payload = json.dumps({
		"b_no": [
			bizno
			]
		})
		headers = {
		'contentType': 'application/json',
		'accept': 'application/json',
		'Content-Type': 'application/json'
		}

		response = requests.request("POST", url, headers=headers, data=payload)

		# print(response.text)
		# rescode = response.getcode()

        # print(docname)
        # credit_check1 = frappe.get_doc('Credit Check',docname)
		if (response.status_code == 200):
			res = json.loads(response.content)
			# print(json.dumps(res['data'][0]['b_no']))
			# response_body = response.read().decode("utf-8")
			# print(response_body)
			# soup = BeautifulSoup(response_body, "xml")
			# smpcbmantrtcntn = (soup.find_all(name="smpcBmanTrtCntn"))[0].text.strip()
			# smpcbmanengltrtcntn = (soup.find_all(name="smpcBmanEnglTrtCntn"))[0].text.strip()
			# trtcntn = (soup.find_all(name="trtCntn"))[0].text.strip()
			# nrgtTxprYn = (soup.find_all(name="nrgtTxprYn"))[0].text.strip()
			# customer_doc = frappe.new_doc('Customer')
			# # print(smpcbmantrtcntn+"\n"+trtcntn+"\n"+nrgtTxprYn+"\n"+smpcbmanengltrtcntn)
			# customer_doc.home_tax_msg = smpcbmanengltrtcntn
			# customer_doc.tax_id = bizno
			# customer_doc.taxation_type = trtcntn
			# customer_doc.home_tax_date = yyyymmdd
			# customer_doc.home_tax_yn = nrgtTxprYn


			customer_doc = frappe.new_doc('Customer')
			# customer_doc.home_tax_msg = json.dumps(res['data'][0]['b_stt'],ensure_ascii=False)
			customer_doc.home_tax_msg = res['data'][0]['b_stt']
			# customer_doc.tax_id = json.dumps(res['data'][0]['b_no'],ensure_ascii=False)
			customer_doc.tax_id = res['data'][0]['b_no']
			# customer_doc.taxation_type = json.dumps(res['data'][0]['tax_type'],ensure_ascii=False)
			customer_doc.taxation_type = res['data'][0]['tax_type'] 
			if res['data'][0]['b_stt_cd'] == '03':
				customer_doc.home_tax_date = res['data'][0]['end_dt'] 
				customer_doc.disabled = 1
			else:
				customer_doc.home_tax_date = yyyymmdd
			# customer_doc.home_tax_yn = json.dumps(res['data'][0]['utcc_yn'],ensure_ascii=False)
			customer_doc.home_tax_yn =  res['data'][0]['utcc_yn']
			


	return customer_doc