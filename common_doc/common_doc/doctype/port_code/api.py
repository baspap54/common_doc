from __future__ import unicode_literals
from email import header

import frappe
import requests
from bs4 import BeautifulSoup

# bench execute common_doc.common_doc.doctype.port_code.api.get_unlocode_port --kwargs "{'country_cd':'us'}"

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
				if list_td[4].text.strip() != '':
					port_doc.sub_div = list_td[1].get_text()[0:2]+"-"+list_td[4].text.strip()
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
				if list_td[4].text.strip() != '':
					port_doc.sub_div = list_td[1].get_text()[0:2]+"-"+list_td[4].text.strip()
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


# bench execute common_doc.common_doc.doctype.port_code.api.get_unlocode_subdivision --kwargs "{'country_cd':'us'}"
@frappe.whitelist()
def get_unlocode_subdivision(**kwargs):
	# print(kwargs)
	# proj_UTMK = Proj(init='epsg:5178')
	# proj_WGS84 = Proj(init='epsg:4326')
	# country_cd = kwargs.get('country_cd')
	url = 'https://service.unece.org/trade/locode/2022-1%20SubdivisionCodes.htm'
	res = requests.get(url)
	html = res.content
	soup = BeautifulSoup(html, 'lxml')
	# list_tr = soup.find_all(name="tr", attrs={"class": "txtAr"})
	
	list_tr = soup.find_all(name="tr")
	# print(len(list_tr))
	for tr_el in list_tr:
		list_td = tr_el.find_all(name='td')
		if len(list_td)==4 :
			# print(list_td[0].get_text())
			if not frappe.db.exists('Sub Division',list_td[0].get_text()+"-"+list_td[1].get_text()):
				sub_div_doc = frappe.new_doc('Sub Division')
				sub_div_doc.country_code = list_td[0].get_text()
				sub_div_doc.country = frappe.db.get_value('Country', {'code': list_td[0].get_text()},'country_name')
				sub_div_doc.sub_division_code = list_td[1].get_text()
				sub_div_doc.sub_division_name = list_td[2].get_text()
				sub_div_doc.sub_division_type = list_td[3].get_text()
				sub_div_doc.insert(
					ignore_permissions=True, # ignore write permissions during insert
					ignore_links=True, # ignore Link validation in the document
					ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
					ignore_mandatory=True 
				) 

		# if len(list_td)==11 and list_td[0].get_text() != 'Ch' and list_td[1].text.strip()[4:7] != '':
		# 	if frappe.db.exists('Sub Division',(list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]):
		# 		port_doc = frappe.get_doc('Sub Division' ,(list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7])

		# 		port_doc.port_name = list_td[2].get_text()
		# 		port_doc.iata = list_td[8].text.strip()
		# 		port_doc.sub_div = list_td[4].text.strip()
		# 		if list_td[4].text.strip() != '':
		# 			port_doc.title = (list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]+'/'+list_td[2].get_text()+'/'+list_td[4].text.strip()
		# 		else:
		# 			port_doc.title = (list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]+'/'+list_td[2].get_text()

		# 		if list_td[5].get_text()[0:1] == '1':	
		# 			port_doc.sea_port = 1
		# 		else:
		# 			port_doc.sea_port = 0
				
		# 		if list_td[5].get_text()[1:2] == '2':
		# 			port_doc.rail_terminal = 1
		# 		else:
		# 			port_doc.rail_terminal = 0

		# 		if list_td[5].get_text()[2:3] == '3':
		# 			port_doc.road_terminal = 1
		# 		else:
		# 			port_doc.road_terminal = 0

		# 		if list_td[5].get_text()[3:4] == '4':
		# 			port_doc.airport = 1
		# 		else:
		# 			port_doc.airport = 0

		# 		if list_td[5].get_text()[4:5] == '5':
		# 			port_doc.postal_exchange_office = 1
		# 		else:
		# 			port_doc.postal_exchange_office = 0

		# 		if list_td[5].get_text()[5:6] == '6':
		# 			port_doc.mulitmodal_functions = 1
		# 		else:
		# 			port_doc.mulitmodal_functions = 0

		# 		if list_td[5].get_text()[6:7] == '7':
		# 			port_doc.fixed_transport_functions = 1
		# 		else:
		# 			port_doc.fixed_transport_functions = 0

		# 		if list_td[5].get_text()[7:8] == 'B':
		# 			port_doc.border_crossing = 1
		# 		else:
		# 			port_doc.border_crossing = 0

		# 		port_doc.status = list_td[6].get_text()
		# 		port_doc.iata = list_td[8].text.strip()

		# 		if list_td[6].get_text()[0:1] == 'A':
		# 			port_doc.use_yn ='Y'
		# 		else:
		# 			port_doc.use_yn ='N'
		# 		port_doc.description = list_td[10].get_text()
		# 		port_doc.country = frappe.db.get_value('Country',{'code':list_td[1].get_text()[0:2]},'country_name')
		# 		Latitude = 0.000
		# 		Longitude = 0.000
		# 		port_doc.coordinates = list_td[9].text.strip()
		# 		if list_td[9].text.strip() != '':
		# 			# print("["+list_td[9].get_text()+"]") 
		# 			Latitude_minute = int(list_td[9].get_text()[2:4])
		# 			Longitude_minute = int(list_td[9].get_text()[9:11])
		# 			Latitude_degree = int(list_td[9].get_text()[0:2])
		# 			Longitude_degree = int(list_td[9].get_text()[6:9])
		# 			Latitude =  Latitude_degree 
		# 			Longitude = Longitude_degree
		# 			if Latitude_minute >0 :
		# 				Latitude += Latitude_minute/60
		# 			if list_td[9].get_text()[4:5] == 'S':
		# 				Latitude = Latitude *(-1)
		# 			if Longitude_minute >0 :
		# 				Longitude += Longitude_minute/60
		# 			if list_td[9].get_text()[11:12] =='W':
		# 				Longitude = Longitude * (-1)

		# 			port_doc.location = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":['+str(Longitude) +','+str(Latitude) +']}}]}'
		# 		port_doc.latitude = Latitude
		# 		port_doc.longitude = Longitude
		# 		port_doc.save()

		# 	else:
		# 		port_doc = frappe.new_doc('Port Code')
		# 		port_doc.country_code = (list_td[1].get_text())[0:2]
		# 		port_doc.port_code = (list_td[1].get_text())[4:7]
		# 		port_doc.port_name = list_td[2].get_text()
		# 		port_doc.iata = list_td[8].text.strip()
		# 		port_doc.sub_div = list_td[4].text.strip()
		# 		if list_td[4].text.strip() != '':
		# 			port_doc.title = (list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]+'/'+list_td[2].get_text()+'/'+list_td[4].text.strip()
		# 		else:
		# 			port_doc.title = (list_td[1].get_text())[0:2]+(list_td[1].get_text())[4:7]+'/'+list_td[2].get_text()
		# 		if list_td[5].get_text()[0:1] == '1':	
		# 			port_doc.sea_port = 1
		# 		else:
		# 			port_doc.sea_port = 0
				
		# 		if list_td[5].get_text()[1:2] == '2':
		# 			port_doc.rail_terminal = 1
		# 		else:
		# 			port_doc.rail_terminal = 0

		# 		if list_td[5].get_text()[2:3] == '3':
		# 			port_doc.road_terminal = 1
		# 		else:
		# 			port_doc.road_terminal = 0

		# 		if list_td[5].get_text()[3:4] == '4':
		# 			port_doc.airport = 1
		# 		else:
		# 			port_doc.airport = 0

		# 		if list_td[5].get_text()[4:5] == '5':
		# 			port_doc.postal_exchange_office = 1
		# 		else:
		# 			port_doc.postal_exchange_office = 0

		# 		if list_td[5].get_text()[5:6] == '6':
		# 			port_doc.mulitmodal_functions = 1
		# 		else:
		# 			port_doc.mulitmodal_functions = 0

		# 		if list_td[5].get_text()[6:7] == '7':
		# 			port_doc.fixed_transport_functions = 1
		# 		else:
		# 			port_doc.fixed_transport_functions = 0

		# 		if list_td[5].get_text()[7:8] == 'B':
		# 			port_doc.border_crossing = 1
		# 		else:
		# 			port_doc.border_crossing = 0

		# 		port_doc.status = list_td[6].get_text()
		# 		port_doc.iata = list_td[8].text.strip()

		# 		if list_td[6].get_text()[0:1] == 'A':
		# 			port_doc.use_yn ='Y'
		# 		else:
		# 			port_doc.use_yn ='N'
		# 		port_doc.description = list_td[10].get_text()
		# 		port_doc.country = frappe.db.get_value('Country',{'code':list_td[1].get_text()[0:2]},'country_name')
		# 		Latitude = 0.000
		# 		Longitude = 0.000
		# 		port_doc.coordinates = list_td[9].text.strip()
		# 		if list_td[9].text.strip() != '':
		# 			# print("["+list_td[9].get_text()+"]") 
		# 			Latitude_minute = int(list_td[9].get_text()[2:4])
		# 			Longitude_minute = int(list_td[9].get_text()[9:11])
		# 			Latitude_degree = int(list_td[9].get_text()[0:2])
		# 			Longitude_degree = int(list_td[9].get_text()[6:9])
		# 			Latitude =  Latitude_degree 
		# 			Longitude = Longitude_degree
		# 			if Latitude_minute >0 :
		# 				Latitude += Latitude_minute/60
		# 			if list_td[9].get_text()[4:5] == 'S':
		# 				Latitude = Latitude *(-1)
		# 			if Longitude_minute >0 :
		# 				Longitude += Longitude_minute/60
		# 			if list_td[9].get_text()[11:12] =='W':
		# 				Longitude = Longitude * (-1)

		# 			port_doc.location = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":['+str(Longitude) +','+str(Latitude) +']}}]}'
		# 		port_doc.latitude = Latitude
		# 		port_doc.longitude = Longitude
				

		# 		port_doc.insert(
		# 			ignore_permissions=True, # ignore write permissions during insert
		# 			ignore_links=True, # ignore Link validation in the document
		# 			ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
		# 			ignore_mandatory=True 
		# 		) 
		# for td_el in list_td:
		# 	# print(td_el.get_text())
		# 	print(td_el)