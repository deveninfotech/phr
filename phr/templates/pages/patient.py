
from __future__ import unicode_literals
import frappe
from frappe.core.doctype.user.user import STANDARD_USERS
from frappe.utils import cint,cstr
import json
import requests
import os
import datetime


"""
	read json for paticular to get the fields also get values if available 
"""	
@frappe.whitelist(allow_guest=True)
def get_data_to_render(data=None,entityid=None):
	json_data, fields, values, tab = None, None, None, None
	print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	print data
	print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	if data:
		data = json.loads(data)
	print "======before dict check ========="
	print data
	print "================================="

	if isinstance(data, dict):
		if not data.get('file_name'):
			json_data = data
			
		else:
			json_data = get_json_data(data.get('file_name'))	

		if data.get('values'):
			json_data['values'] = data.get('values')

		if data.get('method'):
			data = {"method" : data.get('method') }
		else:
			data = data

	if json_data:
		print "----------------------------------"
		print json_data.get(data.get('param'))
		print "===================================="
		fields = json_data.get(data.get('param')) if json_data.get(data.get('param')) else json_data.get('fields')

		print "----------------fields--------------------"
		print fields
		print "------------------------------------------"

		print "@@@@@@@@ values @@@@"
		print json_data
		print "@@@@@@@@@@@@@@@@@@@@"
		tab = json_data.get('tab')
		values = get_values(data,entityid) if not json_data.get('values') else json_data.get('values')

		print "*************values*************"
		print values

	return fields, values, tab
	
@frappe.whitelist(allow_guest=True)	
def get_json_data(file_name):
	fn=file_name+'.json'
	print os.path.join(os.path.dirname(__file__), fn)
	with open(os.path.join(os.path.dirname(__file__), fn), "r") as json_data:
		json_data = json.loads(json_data.read())

	return json_data

def write_json_data(file_name,data):
	with open(os.path.join(os.path.dirname(__file__), file_name +".json"),'w+') as txtfile:
		txtfile.write(json.dumps(data, indent=1, sort_keys=True))

"""
	get data generic method from all db's 
	return plain dictionary 
"""	
def get_values(data,entityid=None):
	print entityid, data
	if entityid:
		url=get_url(data)
		args=get_args(entityid)
		values=get_data(url,args)
		return 	values
	return {}

def get_args(entityid):
	data={"entityid":entityid}
	args=json.dumps(data)
	return args


"""
	get values from solr
"""
def get_data(url,data):
	request_type="POST"
	url=url
	from phr.phr.phr_api import get_response
	response=get_response(url,data,request_type)
	print "-----------------resr-1-----------------------"
	print response
	if response:
		res=json.loads(response.text)
		print res
		data=res["list"][0]
		return data
	else:
		return "No data"
	

"""
	get api url
"""
def get_url(data):
	method=get_method(data)
	base_url=get_base_url()
	url=base_url+method
	return url


"""
	Solr api address
"""
@frappe.whitelist(allow_guest=True)
def get_base_url():
	# return "http://192.168.5.18:9090/phr-api/"
	return "http://88.198.52.49:7974/phr-api/"

"""
Method to get name of method in solr database.contains dictionary or map.
"""
def get_method(data):
	method_dic={"profile":"searchProfile", "event":"searchEvent", "visit":"searchVisit", "provider":"searchProvider"}
	return method_dic.get(data.get('method'))


	
@frappe.whitelist(allow_guest=True)
def get_master_details(doctype):
	import itertools 
	ret = frappe.db.sql("""select name from `tab%s` 
		order by creation desc """%doctype,as_list=1,debug=1)
	return list(itertools.chain(*ret))


@frappe.whitelist(allow_guest=True)
def send_phrs_mail(recipient,subject, template, add_args):

	"""send mail with login details"""
	from frappe.utils.user import get_user_fullname
	from frappe.utils import get_url

	title = frappe.db.get_default('company') or ""

	full_name = get_user_fullname(frappe.session['user'])
	if full_name == "Guest":
		full_name = "Administrator"

	args = {
		'title': title,
		'user_fullname': full_name
	}

	args.update(add_args)

	sender = frappe.session.user not in STANDARD_USERS and frappe.session.user or None

	frappe.sendmail(recipients=recipient, sender=sender, subject=subject,
		message=frappe.get_template(template).render(args))

@frappe.whitelist(allow_guest=True)
def get_formatted_date_time(strdate=None):
	if strdate:
		return datetime.datetime.strptime(strdate,"%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y %H:%M')

@frappe.whitelist(allow_guest=True)
def formatted_date(strdate=None):
	if strdate:
		return datetime.datetime.strptime(strdate,"%Y-%m-%d").strftime('%d/%m/%Y')

@frappe.whitelist(allow_guest=True)
def get_sms_template(name,args):
	import re
	template=frappe.db.get_value("Message Templates",{"name":name},"message_body")
	tempStr = ""
	if template:
		for key in re.findall(r"(?<=\[)(.*?)(?=\])",template):
			old = "[%s]"%key
			new = cstr(args.get(key))
			template = template.replace(old, new)
		return template

