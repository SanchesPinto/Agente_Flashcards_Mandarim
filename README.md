Markdown

# 🇨🇳 Agente IA: Gerador de Flashcards de Mandarim

Um pipeline automatizado e multimodal para criação de flashcards de mandarim focados no Anki. Este projeto recebe uma lista de vocabulário em linguagem natural e utiliza Inteligência Artificial para gerar traduções contextuais, buscar imagens representativas, sintetizar áudio nativo e empacotar tudo em um arquivo `.apkg` pronto para importação.

## ✨ Arquitetura e Features

O projeto foi construído utilizando uma arquitetura modular, onde cada etapa do pipeline é tratada por um serviço especialista:

* **🧠 LLM Agent (OpenAI):** Utiliza o modelo `gpt-4o-mini` com *Structured Outputs* (via Pydantic) para garantir a integridade dos dados. Gera Hanzi, Pinyin, traduções focadas no aprendizado, frases de exemplo e define tags baseadas no nível HSK.
* **🖼️ Visão (Pexels API):** O LLM gera termos de busca otimizados em inglês, que são enviados à API do Pexels para capturar imagens contextuais gratuitas e de alta qualidade.
* **🗣️ Voz Nativa (Edge-TTS):** Utiliza a infraestrutura de nuvem da Microsoft (Edge TTS) de forma assíncrona para gerar áudios neurais ultrarrealistas (Voz: *Xiaoxiao*), separando os áudios da palavra isolada e da frase de exemplo.
* **📦 Empacotamento (Genanki):** Aplica o *Princípio da Informação Mínima*. A partir de 1 palavra, o sistema gera múltiplos cartões interligados (Leitura, Audição, Visual, Tradução Reversa e Contexto), compilando tudo em um arquivo `.apkg` nativo do Anki.

## 🛠️ Pré-requisitos e Instalação

Certifique-se de ter o Python 3.8+ instalado.

1. Clone o repositório:

```bash

git clone [https://github.com/seu-usuario/nome-do-repo.git](https://github.com/seu-usuario/nome-do-repo.git)
cd nome-do-

```


2. Instale as dependências:


```bash
pip install openai pydantic requests edge-tts genanki

```

3. Configure suas variáveis de ambiente. Crie um arquivo .env na raiz do projeto ou exporte no seu terminal:

```bash
export OPENAI_API_KEY="sk-sua-chave-openai"
export PEXELS_API_KEY="sua-chave-pexels"
```

📂 Estrutura do Projeto

A lógica principal foi separada em módulos para facilitar o trabalho em equipe e evitar conflitos:

```bash
/
├── main.py                   # Orquestrador do pipeline
├── modulos/                  
│   ├── __init__.py
│   ├── llm_agent.py          # Integração OpenAI e validação Pydantic
│   ├── gerador_audio.py      # Microsserviço assíncrono do Edge-TTS
│   └── gerador_apkg.py       # Templates HTML/CSS e lógica do Genanki
└── media_temp/               # Pasta de debug (armazena mídias temporárias)
```

🚀 Como Usar

    Abra o arquivo main.py.

    Edite a variável lista_teste com o vocabulário que deseja estudar (máximo de 10 palavras por lote para segurança da API):

Python

lista_teste = "saber, comprar, dinheiro, restaurante"

    Execute o orquestrador:


python main.py

    O console exibirá o progresso de cada etapa (IA -> Imagem -> Áudios -> Genanki).

    Ao finalizar, dê um clique duplo no arquivo Meus_Flashcards_Mandarim.apkg gerado na raiz do projeto para abrir diretamente no Anki!

⚠️ Notas de Desenvolvimento

    Hard Limits: Há uma trava de segurança no llm_agent.py que recusa processar mais de 10 palavras por vez para evitar custos acidentais de API.

    Filtro de Conteúdo: O prompt do sistema está configurado para recusar termos ofensivos ou desrespeitosos.

    Debug Visual: Os arquivos de áudio (.mp3) e imagem (.jpg) permanecem salvos na pasta media_temp após a execução. Use esta pasta para auditar a qualidade da mídia sem precisar importar o baralho no Anki.


***