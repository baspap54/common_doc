from __future__ import unicode_literals
from email import header

import locale
import frappe
import random
import string
import requests
import json
import os
import time
import requests
from urllib import parse

@frappe.whitelist()
def get_postal_code(**kwargs):
	# print("get_calendar")
	# print(kwargs)
	
    country_cd = kwargs.get('country_cd')
    start = kwargs.get('start')
    rows = kwargs.get('rows')
    admin_name1 = str(kwargs.get('admin_name1'))
    # https://data.opendatasoft.com/api/records/1.0/search/?dataset=geonames-postal-code%40public&q=&lang=EN&rows=5&facet=country_code&facet=admin_name1&facet=admin_code1&facet=admin_name2&facet=admin_code2&facet=admin_name3&facet=admin_code3&refine.country_code=KR
    url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=geonames-postal-code%40public&q=&lang=EN&rows="+rows+"&start="+start+"&facet=country_code&facet=admin_name1&facet=admin_code1&facet=admin_name2&facet=admin_code2&facet=admin_name3&facet=admin_code3&refine.country_code="+country_cd
    if kwargs.get('admin_name1') and str(kwargs.get('admin_name1'))!="None":
        url = url+"&refine.admin_name1="+parse.quote(str(kwargs.get('admin_name1')))
    if kwargs.get('admin_name2'):
        url = url+"&refine.admin_name2="+parse.quote(str(kwargs.get('admin_name2')))
    print(url)
    resp = requests.get(url)

    country_name = ""
        
    if (resp.status_code == 200):
        res = json.loads(resp.content)
    
        print(int(res["nhits"]))
            # print(res["records"])
        for postal in res['records']:
            condition_dict ={}
            condition_dict["country_code"] = json.dumps(postal['fields']["country_code"],ensure_ascii=False).replace('\"','')
            condition_dict["postal_code"] = json.dumps(postal['fields']["postal_code"],ensure_ascii=False).replace('\"','')
            condition_dict["place_name"] = json.dumps(postal['fields']["place_name"],ensure_ascii=False).replace('\"','')
            
            for key, value in postal['fields'].items():
                if str(key) == "admin_name1":
                    condition_dict["admin_name1"] = value
                if str(key) == "admin_name2":
                    condition_dict["admin_name2"] = value
                if str(key) == "admin_name3":
                    condition_dict["admin_name3"] = value
                if str(key) == "admin_code1":
                    condition_dict["admin_code1"] = value
                if str(key) == "admin_code2":
                    condition_dict["admin_code2"] = value
                if str(key) == "admin_code3":
                    condition_dict["admin_code3"] = value
                if str(key) == "latitude":
                    condition_dict["latitude"] =value
                if str(key) == "longitude":
                    condition_dict["longitude"] = value
                if str(key) == "accuracy":
                    condition_dict["accuracy"] = value
            
            if not frappe.db.exists('Postal Code',condition_dict,cache=True):
                postal_doc = frappe.new_doc('Postal Code')
                print(json.dumps(postal['fields']["postal_code"]),json.dumps(postal['fields']["place_name"],ensure_ascii=False).replace('\"',''))
                postal_doc.country_code  = json.dumps(postal['fields']["country_code"],ensure_ascii=False).replace('\"','')  
                if not country_name:
                    country_name = frappe.db.get_value('Country',{'code':json.dumps(postal['fields']["country_code"],ensure_ascii=False).replace('\"','') },'country_name')
                    postal_doc.country = country_name
                else:
                    postal_doc.country = country_name
                postal_doc.postal_code = json.dumps(postal['fields']["postal_code"],ensure_ascii=False).replace('\"','')  
                postal_doc.place_name = json.dumps(postal['fields']["place_name"],ensure_ascii=False).replace('\"','')  
                for key, value in postal['fields'].items():
                    if str(key) == "admin_name1":
                        postal_doc.admin_name1 = value
                    if str(key) == "admin_name2":
                        postal_doc.admin_name2 = value
                    if str(key) == "admin_name3":
                        postal_doc.admin_name3 = value
                    if str(key) == "admin_code1":
                        postal_doc.admin_code1 = value
                    if str(key) == "admin_code2":
                        postal_doc.admin_code2 = value
                    if str(key) == "admin_code3":
                        postal_doc.admin_code3 = value
                    if str(key) == "latitude":
                        postal_doc.latitude = value
                    if str(key) == "longitude":
                        postal_doc.longitude = value
                    if str(key) == "accuracy":
                        postal_doc.accuracy = value
                postal_doc.location = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":['+str(postal_doc.longitude) +','+str(postal_doc.latitude) +']}}]}'
                postal_doc.insert(
                        ignore_permissions=True, # ignore write permissions during insert
                        ignore_links=True, # ignore Link validation in the document
                        ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
                        ignore_mandatory=True 
                    ) 
        return  int(res["nhits"])- int(rows)
           
@frappe.whitelist()
def get_admin_name(**kwargs):
    country_cd = kwargs.get('country_cd')
    url1 = 'https://data.opendatasoft.com/api/records/1.0/search/?dataset=geonames-postal-code%40public&q=&lang=EN&rows=5&facet=country_code&facet=admin_name1&facet=admin_code1&facet=admin_name2&facet=admin_code2&facet=admin_name3&facet=admin_code3&refine.country_code='+country_cd
    print(url1)
    resp1 = requests.get(url1)
    start_no = 0
    rows_no =10000
    if (resp1.status_code == 200):
        res1 = json.loads(resp1.content)
        for postal_group in res1['facet_groups']:
            if json.dumps(postal_group['name'],ensure_ascii=False).replace('\"','')  == 'admin_name1':
                # print(json.dumps(postal_group['facets']))
                for admin1 in postal_group['facets']:
                    print(admin1['name'],int(admin1['count']))
                    admin_name1 = ""
                    admin_name1 = admin1['name']
                    if int(admin1['count']) >10000:
                        url2 = url1+"&refine.admin_name1="+admin_name1
                        print(url2)
                        resp2 = requests.get(url2)
                        if (resp2.status_code == 200):
                            res2 = json.loads(resp2.content)
                            for postal_group2 in res2['facet_groups']:
                                if json.dumps(postal_group2['name'],ensure_ascii=False).replace('\"','')  == 'admin_name2':
                                    # print(json.dumps(postal_group['facets']))
                                    for admin2 in postal_group2['facets']:
                                        print(admin2['name'])
                                        print(admin2['name'],int(admin2['count']))
                                        get_postal_code(country_cd=country_cd,rows=str(rows_no),start=str(start_no),admin_name1=admin_name1,admin_name2=admin2['name'])
                                        frappe.db.commit()
                                        time.sleep(5)
                    else:
                        get_postal_code(country_cd=country_cd,rows=str(rows_no),start=str(start_no),admin_name1=admin1['name'])
                        frappe.db.commit()
                        time.sleep(5)
                    

                        



# bench execute common_doc.common_doc.doctype.postal_code.api.get_postal_code --kwargs "{'country_cd':'KR','rows':'10000','start':'0','admin_name1':'서울특별시'}"
# bench execute common_doc.common_doc.doctype.postal_code.api.get_admin_name --kwargs "{'country_cd':'KR'}"
@frappe.whitelist()
def get_admin1_list(country_code):
    # print(country_code)
    admin1_list = frappe.db.get_list('Postal Code',
        fields=['count(name) as count', 'admin_name1','admin_code1'],
        filters={'country_code':country_code},
        group_by='admin_name1',
        order_by='admin_name1'
    )
    # for admin1 in admin1_list:
    #     print(admin1)
    return admin1_list

@frappe.whitelist()
def get_admin2_list(country_code,admin_name1):
    # print(admin_name1)
    admin2_list = frappe.db.get_list('Postal Code',
        fields=['count(name) as count', 'admin_name2','admin_code2'],
        filters={'country_code':country_code,'admin_name1':admin_name1},
        group_by='admin_name2',
        order_by='admin_name2'
    )
    # for admin2 in admin2_list:
    #     print(admin2)
    return admin2_list

@frappe.whitelist()
def get_admin3_list(**args):
    # print(admin_name1)
    country_code = args.get('country_code')
    admin_name1 = args.get('admin_name1')
    admin_name2 = args.get('admin_name2')
    lv_filters = {}
    if country_code:
        lv_filters['country_code'] = country_code
    if admin_name1:
        lv_filters['admin_name1'] = admin_name1
    if admin_name2:
        lv_filters['admin_name2'] = admin_name2
    admin3_list = frappe.db.get_list('Postal Code',
        fields=['count(name) as count', 'admin_name3','admin_code3'],
        filters=lv_filters,
        group_by='admin_name3',
        order_by='admin_name3'
    )
    # for admin2 in admin2_list:
    #     print(admin2)
    return admin3_list

@frappe.whitelist()
def get_places_list(**args):
    # print(admin_name1)
    country_code = args.get('country_code')
    admin_name1 = args.get('admin_name1')
    admin_name2 = args.get('admin_name2')
    admin_name3 = args.get('admin_name3')
    lv_filters = {}
    if country_code:
        lv_filters['country_code'] = country_code
    if admin_name1:
        lv_filters['admin_name1'] = admin_name1
    if admin_name2:
        lv_filters['admin_name2'] = admin_name2
    if admin_name3:
        lv_filters['admin_name3'] = admin_name3

    # print(lv_filters)

    places_list = frappe.db.get_list('Postal Code',
        fields=[ 'place_name'],
        filters=lv_filters,
        group_by='place_name',
        order_by='place_name'
    )
    # for place in places_list:
    #     print(place)
    return places_list

@frappe.whitelist()
def get_zip_list(**args):
    # print(admin_name1)
    country_code = args.get('country_code')
    admin_name1 = args.get('admin_name1')
    admin_name2 = args.get('admin_name2')
    admin_name3 = args.get('admin_name3')
    place_name = args.get('place_name')
    lv_filters = {}
    if country_code:
        lv_filters['country_code'] = country_code
    if admin_name1:
        lv_filters['admin_name1'] = admin_name1
    if admin_name2:
        lv_filters['admin_name2'] = admin_name2
    if admin_name3:
        lv_filters['admin_name3'] = admin_name3
    if place_name:
        lv_filters['place_name'] = place_name
    print(lv_filters)

    zip_list = frappe.db.get_list('Postal Code',
        fields=[ 'postal_code','name'],
        filters=lv_filters
    )
    # for place in zip_list:
    #     print(place)
    return zip_list

# bench execute common_doc.common_doc.doctype.postal_code.api.get_admin1_list --kwargs "{'country_code':'US'}"