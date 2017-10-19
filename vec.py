#!/usr/bin/python

import re
import os
import sys
import requests
import json

tag = sys.argv[1]

# regex para validar formato da string no padrao VEC
if re.match('^([0-9]{1,2}\.){2}[0-9]{1,2}(_PRD)?$', tag) is None:
    exit(0)

# url do gitlab, necessario para usar api
url = 'http://gitlab.example.com'
# token de acesso do gitlab
token = '4G7jTzFaX9CUgsdgyPv2'
# usuario permitido
allowed_user = 'devops'

# se conecta na api do gitlab para buscar informacoes
user_id = os.environ['GL_ID'].replace('key-', '')
r = requests.get('%s/api/v3/keys/%s' % (url, user_id), headers={'PRIVATE-TOKEN': token})

# extrai informacoes sobre o usuario
if r.status_code == 200:
    username = json.loads(r.text)['user']['username']
else:
    print 'Nao foi possivel obter usuario'
    exit(1)

# verifica se usuario pode criar tag protegida
if username != allowed_user:
    print 'Usuario %s nao autorizado a criar tags nesse formato' % username
    exit(1)

exit(0)