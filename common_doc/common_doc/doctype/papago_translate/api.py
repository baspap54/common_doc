import frappe
import os
import sys
import json
import urllib.request

@frappe.whitelist()
def get_translate(**args):
    secrets_file = os.path.join(os.getcwd(), 'secrets.json')
    with open(secrets_file) as f:
        secrets = json.load(f)
    client_id = secrets["papago_client_id"]
    client_secret = secrets["papago_client_secret"]
    encText = urllib.parse.quote(args.get('source_text'))
    data = "source="+args.get('source')+"&target="+args.get('target')+"&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    papago_translate = frappe.new_doc('Papago Translate')
    papago_translate.source = args.get('source')
    papago_translate.target = args.get('target')
    papago_translate.source_text = args.get('source_text')
    if (rescode == 200):
        response_body = response.read()
        #print("Log1:"+ response_body.decode('utf-8'))
        res = json.loads(response_body)
        papago_translate.target_text = res['message']['result']['translatedText']
        #print(res['message']['result']['translatedText'])

    else:
        print("Error Code:" + rescode)

    return papago_translate