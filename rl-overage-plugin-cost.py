#!/usr/bin/env python2

import requests
import json
import datetime
import os

#add your RightScale details as environment variables:
# RS_REFRESH_TOKEN
# RS_SERVER
# RS_ACCOUNT_ID
# RIGHTLINK_RATE

#your account ID is in the URL when you're viewing that account in the RightScale UI
#get your refresh token from the RightScale UI under "API Credentials"
#your shard will be either us-3, us-4 or telstra-10
#your overage rate must be in USD eg 0.05

#checks if you're using Rancher Secrets
#when using Rancher, please set the shard as an environment variable in the Rancher UI
print("Checking if you're using Rancher Secrets...")
if os.path.isdir("/run/secrets"):
	print("Secrets directory exists, importing variables...")
	os.environ['RS_ACCOUNT_ID'] = open('/run/secrets/RS_ACCOUNT_ID', 'r').read()
	os.environ['RS_SERVER'] = open('/run/secrets/RS_SERVER', 'r').read()
	os.environ['RS_REFRESH_TOKEN'] = open('/run/secrets/RS_REFRESH_TOKEN', 'r').read()
	os.environ['RIGHTLINK_RATE'] = open('/run/secrets/RIGHTLINK_RATE', 'r').read()

auth_endpoint = 'https://' + os.environ['RS_SERVER'] + '/api/oauth2'
parent_acc = "/api/accounts/" + os.environ['RS_ACCOUNT_ID']
refresh_token = os.environ['RS_REFRESH_TOKEN']
rl_rate = os.environ['RIGHTLINK_RATE']

#works out date range for this month
now = datetime.datetime.now()
month_start = now.isoformat()[:-18] + '01T00:00:00'
end_time =  now.isoformat()[:-7]

#works out your access token for API authentication
auth_headers =	{'X-API-Version': '1.5'}
auth_payload =		{
	'grant_type': 'refresh_token',
	'refresh_token': refresh_token
					}

print('Authenticating...')
auth_call = requests.post(url=auth_endpoint, headers=auth_headers, json=auth_payload)

if auth_call.status_code == 200:
	print('Success!')
else:
	print('Something went wrong...')
	print(auth_call.text)

auth_output = json.loads(auth_call.text)
access_token = auth_output['access_token']

#works out the overage cost
usage_url = 'https://analytics.rightscale.com/api/instances'
usage_headers =		{
	'Authorization': 'Bearer {0}'.format(access_token),
	'Content-Type': 'text/json',
	'X-API-VERSION': '1.0'
					}

instance_filters = 	[
 					{
    "kind": "ca#filter",
    "type": "instance:tag",
    "value": "rs_agent:type=right_link_lite",
    "tag_resource_type": "instances"
  					}
					]

usage_payload = 	{
	'start_time': month_start,
	'end_time': end_time,
	'instance_filters': instance_filters
					}

print('Getting usage...')
usage_call = requests.post(url=usage_url, headers=usage_headers, json=usage_payload)

if usage_call.status_code == 200:
	print('Success!')
else:
	print('Something went wrong...')
	print(usage_call.text)

usage_output = json.loads(usage_call.text)
usage_list = [d['total_usage_hours'] for d in usage_output]
total_hours = sum(usage_list)

if total_hours > 73000:
	total_cost = (total_hours - 73000) * rl_rate

else:
	total_cost = 0

print('Overage cost this month:')
print(total_cost)

#checks if any plugin costs already exist
index_url = 'https://analytics.rightscale.com/api/plugin_costs'

index_headers =		{
	'Authorization': 'Bearer {0}'.format(access_token),
	'Content-Type': 'application/json',
	'X-API-VERSION': '1.0'
					}

print('Checking what plugin costs already exist...')
index_call = requests.get(url=index_url, headers=index_headers)

if index_call.status_code == 200:
	print('Success!')
else:
	print('Something went wrong...')
	print(index_call.text)

index_output = json.loads(index_call.text)
month_now = index_output[0].get("start_time", "")[:-18]

#if no plugin costs exists it creates one for you
if len(index_output) == 0:

	print('No existing plugin cost found - creating one...')

	plugin_url = 'https://analytics.rightscale.com/api/plugin_costs'

	plugin_headers =	{
		'Authorization': 'Bearer {0}'.format(access_token),
		'Content-Type': 'application/json',
		'X-API-VERSION': '1.0'
						}

	plugin_payload =	{
		'account_href': parent_acc,
		'start_time': month_start,
		'total_cost': total_cost,
		'product': 'I&Co RightLink Usage',
  		'product_category': 'Other'
						}

	plugin_call = requests.post(url=plugin_url, headers=plugin_headers, json=plugin_payload)

	if plugin_call.status_code == 200:
		print('Created new plugin cost')
	else:
		print('Something went wrong...')
		print(plugin_call.text)

#if a plugin cost already exists for this month it will update it
elif month_now == end_time[:-12]:

	print('Found existing plugin cost for this month - updating...')

	if index_output[0].get("href", "") != "":
		plugin_id = index_output[0].get("href", "")

		update_url = 'https://analytics.rightscale.com' + plugin_id

		update_headers =	{
			'Authorization': 'Bearer {0}'.format(access_token),
			'Content-Type': 'application/json',
			'X-API-VERSION': '1.0'
							}

		update_payload =	{
			'account_href': parent_acc,
			'start_time': month_start,
			'total_cost': total_cost,
			'product': 'I&Co RightLink Usage',
  			'product_category': 'Other'
							}

		update_call = requests.patch(url=update_url, headers=update_headers, json=update_payload)

		if update_call.status_code == 200:
			print('Updated plugin cost for this month')
		else:
			print('Something went wrong...')
			print(update_call.text)

#if plugin costs exist, but not for this month, it creates one for you
else:

	print('No plugin cost found for this month - creating one...')

	plugin_url = 'https://analytics.rightscale.com/api/plugin_costs'

	plugin_headers =	{
		'Authorization': 'Bearer {0}'.format(access_token),
		'Content-Type': 'application/json',
		'X-API-VERSION': '1.0'
						}

	plugin_payload =	{
		'account_href': parent_acc,
		'start_time': month_start,
		'total_cost': total_cost,
		'product': 'I&Co RightLink Usage',
  		'product_category': 'Other'
						}

	plugin_call = requests.post(url=plugin_url, headers=plugin_headers, json=plugin_payload)

	if plugin_call.status_code == 200:
		print('Created new plugin cost for this month')
	else:
		print('Something went wrong...')
		print(plugin_call.text)
