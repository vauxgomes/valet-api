import requests

import requests as rq

# Atualizar de acordo com a URL do serviço
url = 'http://127.0.0.1:5000/'
endpoint = 'run'

#
data = ['att1', 'att2', '...', 'att3'] # TODO: Colocar um dado real

# POST Request
res = requests.post(f'{url}{endpoint}', json=data)

#
print(f'{url}{endpoint}')
print(res.text)