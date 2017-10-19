# hook-scripts
GitLab Hook scripts!

O script update é uma modificação feita do arquivo update que vem junto com o repositório git a ser clonado.

Houveram duas modificações nele:

## Checar arquivos do commit (a parti da linha 31)
```sh
retorno=$(python custom_hooks/files.py $1 $2 $3)
if [ $? -ne 0 ]; then
    echo "$retorno" >&2
    exit 1
fi
```

O files.py irá checar se foi commitado algum arquivo com extensão inválida:

```python
# Please, set a list of forbidden extensions
extensions=['.zip']
```

## Checar usuário e tag (a partir da linha 58)
```sh
case "$refname","$newrev_type" in
    refs/tags/*,commit)
        # un-annotated tag
        short_refname=${refname##refs/tags/}
        retorno=$(python custom_hooks/vec.py $short_refname)
        if [ $? -ne 0 ]; then
            echo "$retorno" >&2
            exit 1
        fi
        ;;
```

O arquivo vec.py verá se a tag está no padrão VEC. Neste script, apenas um usuário é permitido para criar esse tipo de tag. Isso foi feito para garantir que nenhum outro usuário criará uma tag com versão que poderá enganar o integrador e fazer o deploy por engano de uma versão.

```python
# url do gitlab, necessario para usar api
url = 'http://gitlab.example.com'
# token de acesso do gitlab
token = '4G7jTzFaX9CUgsdgyPv2'
# usuario permitido
allowed_user = 'devops'
```

Neste trecho, é necessário inserir o TOKEN para acessar a API do Gitlab e validar o usuário permitido na variável **allowed_user = 'devops'**. O TOKEN é criado na interface do GitLab.

A url da requisão pode mudar dependendo da versão do GitLab que estiver instalada ( v2/v3/v4 [...] ).
```python 
# se conecta na api do gitlab para buscar informacoes
user_id = os.environ['GL_ID'].replace('key-', '')
r = requests.get('%s/api/v3/keys/%s' % (url, user_id), headers={'PRIVATE-TOKEN': token})
```