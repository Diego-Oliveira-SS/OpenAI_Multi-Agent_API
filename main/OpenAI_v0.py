# chat com OpenAI usando a biblioteca OpenAI Python
# Este código permite interação simples sem memorizar o histórico de mensagens

import os
from openai import OpenAI
import yaml

# Carregar a configuração do arquivo YAML (senha da API)
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Definir variável de ambiente
os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']= config['OPENAI_API_KEY']


os.system('cls')  # Limpa o terminal (use 'clear' para Linux/Mac)

#O chat começa aqui
print("Star chat with OpenAI...")
client = OpenAI()


print("OpenAI client initialized successfully. Print 'quit' to exit.")

#configuração do comportamento do chat (adicione regras aqui)
messages = [
    {"role": "system", "content": "Você é um assistente útil e responde de forma clara."},
    {"role": "system", "content": "Pensará na resposta antes de responder."},
    {"role": "system", "content": "Responda com no máximo 20 palavras."}
    ]

while True: #mantem a conversa ativa
    
    user_input = input("You: ")   #input do usuário

    if user_input.lower() == "quit": # condição de saída
        print("Saindo do chat.")
        break

    messages.append({"role": "user", "content": user_input}) #adiciona a mensagem do usuário à conversa

    # chama o OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=50,
        tools=[]
        )
    
    reply = response.choices[0].message.content # extrai a resposta do assistente

    messages.append({"role": "assistant", "content": reply}) # adiciona a resposta do assistente à conversa
    
    print(f"IA: {reply}")  # exibe a resposta do assistente