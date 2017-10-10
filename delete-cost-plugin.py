#variables you might wanna edit are:
#api_endpoint
#my_refresh_token
#delete_url (add '/:id' eg '/246' to the end to specify which cost plugin to delete)


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
auth_call = requests.post(url=api_endpoint, headers=auth_headers, data=auth_payload)

#prints the response to the terminal so that you know if it worked or if you stuffed it (you want 200)
print auth_call

#now we gotta define what the 'access_token' is ie it's equal to the first part of the JSON response we got from above
resp_str = auth_call.text
resp_dict = json.loads(resp_str)

access_token = resp_dict['access_token']

#API endpoint of the cost plugin you want to update
delete_url = 'https://analytics.rightscale.com/api/plugin_costs/123'

#tell it that you want to use the access token that we got from above as the authorisation
#the content will be JSON format
#and the API version is 1.0 because it's the Cloud Analytics API
delete_headers =	{
	'Authorization': 'Bearer {0}'.format(access_token),
	'Content-Type': 'application/json',
	'X-API-VERSION': '1.0'
					}

#the API call - using DELETE
delete_call = requests.delete(url=delete_url, headers=delete_headers)

#prints the response to the terminal so that you know if it worked or if you stuffed it (you want 204)
print delete_call
