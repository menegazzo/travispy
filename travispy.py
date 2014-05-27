import requests


headers = {
    'User-Agent': 'TravisPy',
    'Accept': 'application/vnd.travis-ci.2+json',
}

host = 'http://api.travis-ci.org'

# Making requests ----------------------------------------------------------------------------------
response = requests.get(host, headers=headers)
print response.json()

# External APIs ------------------------------------------------------------------------------------
response = requests.get(host + '/config', headers=headers)
print response.json()
