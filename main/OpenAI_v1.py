"""
Chat com OpenAI usando a biblioteca OpenAI Python.

Este script implementa um chat simples com memória do lado do cliente,
usando a API de Chat Completions do OpenAI. Ele lê a API key do ambiente
(`OPENAI_API_KEY`) ou, opcionalmente, do arquivo `config.yaml` se existir.
"""

import os
import sys
import platform
from typing import Optional

import yaml
from openai import OpenAI


def load_api_key() -> Optional[str]:
    # 1) Prioriza variável de ambiente
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key:
        return env_key

    # 2) Opcional: tenta carregar de config.yaml, se existir
    cfg_path = "config.yaml"
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            return cfg.get("OPENAI_API_KEY")
        except Exception:
            return None
    return None


def clear_console() -> None:
    try:
        if platform.system().lower().startswith("win"):
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        pass


def main() -> int:
    api_key = load_api_key()
    if not api_key:
        print("Erro: defina a variável de ambiente OPENAI_API_KEY ou crie config.yaml com OPENAI_API_KEY.")
        return 1

    clear_console()
    print("Start chat with OpenAI... (digite 'quit' para sair)")

    client = OpenAI(api_key=api_key)

    # Mensagens de sistema (regras do assistente)
    messages = [
        {"role": "system", "content": "Você é um assistente útil e responde de forma clara."},
        {"role": "system", "content": "Pense na resposta antes de responder."},
        {"role": "system", "content": "Responda com no máximo 20 palavras."},
        # Para exibir tokens, podemos consultar response.usage depois
    ]

    # Loop de conversa
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo do chat.")
            break

        if user_input.lower() in {"quit", "sair", "exit"}:
            print("Saindo do chat.")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            # Use um modelo disponível e econômico. Ajuste conforme necessário.
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=80,
                temperature=0.7,
            )
        except Exception as e:
            print(f"Erro ao chamar a API: {e}")
            # Opcionalmente remova a última mensagem do usuário se quiser repetir
            continue

        reply = completion.choices[0].message.content if completion.choices else "(sem resposta)"
        messages.append({"role": "assistant", "content": reply})
        print(f"IA: {reply}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

