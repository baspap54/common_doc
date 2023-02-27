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
import re

# bench execute common_doc.api.get_bl_info_from_shipmentlink --kwargs "{'bl_no':'040300049820'}"
#  bench execute common_doc.api.get_bl_info_from_shipmentlink --kwargs "{'cntr_no':'EITU1764645'}"
@frappe.whitelist()
def get_bl_info_from_shipmentlink(**kwargs):
	bl_no = kwargs.get('bl_no')
	cntr_no = kwargs.get('cntr_no')
	result={}
	url1 = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'
	if bl_no:
		data = {
			'TYPE': 'BL',
			'BL': bl_no,
			'CNTR':'',
			'bkno':'',
			'query_bkno':'',
			'query_rvs':'',
			'query_docno':'',
			'query_seq':'',
			'PRINT':'',
			'SEL':'s_bl',
			'NO': bl_no
		}
	if cntr_no:
		data = {
			'TYPE': 'CNTR',
			'BL': '',
			'CNTR':cntr_no,
			'bkno':'',
			'query_bkno':'',
			'query_rvs':'',
			'query_docno':'',
			'query_seq':'',
			'PRINT':'',
			'SEL':'s_cntr',
			'NO': cntr_no
		}
	res1 = requests.post(url1, data=data)
	html = res1.content
	# print(html)
	soup = BeautifulSoup(html, 'html.parser')
	list_tables = soup.find_all(name='table', attrs={"class": "ec-table ec-table-sm"})
	list_tables2 = soup.find_all(name='table', attrs={"class": "ec-table"})
	list_tds3 = soup.find_all(name='td', attrs={"class": "ec-fs-16b","align":"left"})
	# print(list_tds3)
	for list_td3 in list_tds3:
		# print(list_td3.get_text().strip()[0:40])
		if list_td3.get_text().strip()[0:40] == "Estimated Date of Arrival at Destination":
			print(list_td3.find_all(name='font')[0].get_text().strip())
	# print(len(list_tables))
	if bl_no:
		# for list_table2 in list_tables2:
		# 	list_trs2 = list_table2.find_all(name='tr')
			# if "Container(s) information on B/L and Current Status" == list_trs[0].find_all(name='td')[0].get_text().strip():
			# 	pass
		for list_table in list_tables:
	# 		# print(list_table)
			list_trs = list_table.find_all(name='tr')
	# 		# print(list_trs[0].find_all(name='td')[0].get_text().strip())
			if "Container(s) information on B/L and Current Status" == list_trs[0].find_all(name='td')[0].get_text().strip():
				print(list_trs[0].find_all(name='td')[0].get_text().strip())
	# 			# list_trs[2].find_all(name='td')[0].get_text().strip()
	# 			# list_trs[2].find_all(name='td')[7].get_text().strip()
	# 			# list_trs[2].find_all(name='td')[8].get_text().strip()
				url2 = "https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do"
				data2 = {
					'TYPE': 'GetDispInfo',
					'Item': 'PickupRef',
					'BL': bl_no,
					'firstCtnNo':list_trs[2].find_all(name='td')[0].get_text().strip()
				}
				res2 = requests.post(url2, data=data2)
				html2 = res2.content

				soup2 = BeautifulSoup(html2, 'html.parser')
				list_tr_details = soup2.find_all(name='tr')

				# print(len(list_trs))
				if len(list_tr_details)>1:
					result = {
						"cntr":list_trs[2].find_all(name='td')[0].get_text().strip(),
						"mbl" : bl_no,
						"status": list_trs[2].find_all(name='td')[7].get_text().strip(),
						"eta": list_trs[2].find_all(name='td')[8].get_text().strip(),
						"port":list_tr_details[1].find_all(name='th')[1].get_text().strip()
					}
				else:
					result = {
						"cntr":list_trs[2].find_all(name='td')[0].get_text().strip(),
						"mbl" : bl_no,
						"status": list_trs[2].find_all(name='td')[7].get_text().strip(),
						"eta": list_trs[2].find_all(name='td')[8].get_text().strip(),
						"port":''
					}
	return result

	# /html/body/div[5]/center/table[3]/tbody/tr/td/table[3]/tbody/tr[3]/td[8]
	# /html/body/div[5]/center/table[3]/tbody/tr/td/table[3]