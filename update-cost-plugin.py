#variables you might wanna edit are:
#api_endpoint
#my_refresh_token
#update_url (add '/:id' eg '/246' to the end to specify which cost plugin to update)
#account_href
#start_time
#total_cost
#product
#product_category


#import dependancies, libraries, etc, whatever they're called
import requests
import json

#API endpoint to get the access token (choose one: 'telstra-10', 'us-3', or 'us-4')
api_endpoint = 'https://<endpoint>.rightscale.com/api/oauth2'

#refresh token you gotta get from 'API Credentials' in the RightScale UI for whatever account you want to use
my_refresh_token = '<refresh_token>'

#tell it what API version to use - need to use Cloud Management API to authenticate
auth_headers =	{'X-API-Version': '1.5'}

#data in the API call - grant type and the token mentioned above
auth_payload =	{
	'grant_type': 'refresh_token',
	'refresh_token': my_refresh_token
				}

#the API call - using POST
auth_call = requests.post(url=api_endpoint, headers=auth_headers, json=auth_payload)

#prints the response to the terminal so that you know if it worked or if you stuffed it (you want 200)
print auth_call

#now we gotta define what the 'access_token' is ie it's equal to the first part of the JSON response we got from above
resp_str = auth_call.text
resp_dict = json.loads(resp_str)

access_token = resp_dict['access_token']

#API endpoint to create the cost plugin
update_url = 'https://analytics.rightscale.com/api/plugin_costs/123'

#tell it that you want to use the access token that we got from above as the authorisation
#the content will be JSON format
#and the API version is 1.0 because it's the Cloud Analytics API
update_headers =	{
	'Authorization': 'Bearer {0}'.format(access_token),
	'Content-Type': 'application/json',
	'X-API-VERSION': '1.0'
					}

#data in the API call - as explained below in the JSON
update_payload =	{
	'account_href': '/api/accounts/123456',
	'start_time': '2017-01-01T00:00:00+00:00',
	'total_cost': '0.077',
	'product': 'Plugin Cost Product',
  	'product_category': 'Other'
					}

#the API call - using PATCH
update_call = requests.patch(url=update_url, headers=update_headers, json=update_payload)

#prints the response to the terminal so that you know if it worked or if you stuffed it (you want 200)
print 'update_call response: ' + update_call.text
print update_call
