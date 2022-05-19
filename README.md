![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PyCharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)
[![CodeQL](https://github.com/Marrowsed/Desafio_Alura3/actions/workflows/codeql.yml/badge.svg)](https://github.com/Marrowsed/Desafio_Alura3/actions/workflows/codeql.yml)
# Desafio_Alura3
#alurachallengebackend3

## ✔️ Técnicas e tecnologias utilizadas

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Django_logo.svg/2560px-Django_logo.svg.png" alt="Logo do Django">

- ``Python``
- ``PostgreSQL``
- ``PyCharm``

## Desafios
- Criar uma Aplicação Web para receber arquivos em .CSV ou .XML e realizar a Validação ✔️
- Realizar um CRUD de Usuários ✔️
- O Usuário só precisa cadastrar Nome e E-mail e receberá a senha por e-mail ✔️
- Todos os usuários podem se remover (exceto a si mesmo) ✔️
- Exclusão Lógica de Usuários ✔️
- Senha Criptografada pelo BCrypt
- Testes Unitários
- Deploy ✔️

<h1> Instalação </h1>
É necessária a Instalação mais recente do <a href="https://www.python.org/downloads/" target="_blank">Python</a>

<h2> Dependências</h2>

````sh
pip install -r requirements.txt
````

<h1> Configuração </h1>
<ol>
  <li> Crie um arquivo `.env` na mesma pasta onde está o arquivo `migrate.py`.</li>
  <li>No seu terminal com o ambiente virtual ativado, execute o comando `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` para gerar uma chave secreta.</li>
  <li>Substitua a chave secreta no arquivo `.env` com a chave gerada na variável `SECRET_KEY`.</li>
  <li>Substitua o endereço do banco de dados no arquivo `.env` com o endereço do banco de dados que você deseja utilizar na variável `DATABASE_URL`.</li>
  <li>Execute o comando `python manage.py migrate` para criar as tabelas do banco de dados.</li>
</ol>

<h1>Rodando o projeto</h1>

```sh
python manage.py runserver
```

O servidor está rodando, visite http://127.0.0.1:8000/ no seu navegador de internet

![Alura](https://media.discordapp.net/attachments/973568663959502888/973568782947737620/Badge_Alura_Challenge_back_First_v3.png?width=701&height=701)
