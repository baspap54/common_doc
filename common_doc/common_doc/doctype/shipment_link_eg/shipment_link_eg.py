# Copyright (c) 2023, John and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
from bs4 import BeautifulSoup

class ShipmentLinkEG(Document):
	def on_update(self):
		# print(self.no_info)
		no_infos = self.no_info.splitlines()
		for no_info in no_infos:
			print(no_info)
			print(len(no_infos))
			if len(self.item)==0:
				url1 = 'https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do'
				data = {
					'TYPE': 'BL',
					'BL': no_info,
					'CNTR':'',
					'bkno':'',
					'query_bkno':'',
					'query_rvs':'',
					'query_docno':'',
					'query_seq':'',
					'PRINT':'',
					'SEL':'s_bl',
					'NO': no_info
				}
				res1 = requests.post(url1, data=data)
				html = res1.content
				eta_date = ""
				# print(html)
				soup = BeautifulSoup(html, 'html.parser')
				list_tables = soup.find_all(name='table', attrs={"class": "ec-table ec-table-sm"})
				list_tds3 = soup.find_all(name='td', attrs={"class": "ec-fs-16b","align":"left"})
				# print(list_tds3)
				for list_td3 in list_tds3:
					# print(list_td3.get_text().strip()[0:40])
					if list_td3.get_text().strip()[0:40] == "Estimated Date of Arrival at Destination":
						# print(list_td3.find_all(name='font')[0].get_text().strip())
						eta_date =list_td3.find_all(name='font')[0].get_text().strip()
				for list_table in list_tables:
			# 		# print(list_table)
					list_trs = list_table.find_all(name='tr')
			# 		# print(list_trs[0].find_all(name='td')[0].get_text().strip())
					if "Container(s) information on B/L and Current Status" == list_trs[0].find_all(name='td')[0].get_text().strip():
						url2 = "https://ct.shipmentlink.com/servlet/TDB1_CargoTracking.do"
						data2 = {
							'TYPE': 'GetDispInfo',
							'Item': 'PickupRef',
							'BL': no_info,
							'firstCtnNo':list_trs[2].find_all(name='td')[0].get_text().strip()
						}
						res2 = requests.post(url2, data=data2)
						html2 = res2.content
			# 			# print(html2)

						soup2 = BeautifulSoup(html2, 'html.parser')
						list_tr_details = soup2.find_all(name='tr')
						port_info =""
						
						if len(list_tr_details)>1:
							port_info = list_tr_details[1].find_all(name='th')[1].get_text().strip()
						# print(len(list_trs))
						if len(list_trs)>2:
							# print(list_trs[2].find_all(name='td')[0].get_text().strip())
							for i in range(2,len(list_trs)):
								# print(list_trs[i].find_all(name='td')[0].get_text().strip())
								child = frappe.get_doc({
									"parentfield": "item",
									"parent":self.name,
									"parenttype": "Shipment Link EG",
									"doctype": "Shipment Link Detail EG" ,
									"cntr":list_trs[i].find_all(name='td')[0].get_text().strip() ,
									"mbl":no_info ,
									"status": list_trs[i].find_all(name='td')[7].get_text().strip(),
									"eta":eta_date,
									"status_date":list_trs[i].find_all(name='td')[8].get_text().strip(),
									"port":port_info
								}).insert(
									ignore_permissions=True, # ignore write permissions during insert
									ignore_links=True, # ignore Link validation in the document
									# ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
									ignore_mandatory=True # insert even if mandatory fields are not set
								)
		self.reload()