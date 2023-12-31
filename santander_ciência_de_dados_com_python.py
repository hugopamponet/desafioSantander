# -*- coding: utf-8 -*-
"""Santander Ciência de Dados com Python.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17hqb9oAngiqMEK2ov44Efa7OFp_Tu0WB
"""

sdw2023_url = 'https://sdw-2023-prd.up.railway.app'

import pandas as pd

df = pd.read_csv('01 - desafio.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

import requests
import json

def get_user(id):
  response = requests.get(f'{sdw2023_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

!pip install openai

key_api_openai = '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'

import os
import openai

openai.api_key = key_api_openai

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content":"Você é um especialista em mercado financeiro."},
    {"role": "user", "content": f"Crie uma mensagem para {user['name']} sobre os melhores investimentos para o mês (máximo de 100 caracteres)"}
    ]
  )
return completion.choices[0].message.content.strip('\"')


for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })

import json

from sqlalchemy.sql.expression import update
def update_user(user):
  response = requests.put(f"{sdw2023_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} update? {success}!")