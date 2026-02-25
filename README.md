# 📖 LLMs e RAGS

Este projeto utiliza Python 3.12, LangChain e LM Studio para experimentos com LLMs e RAG. A configuração inclui criação de ambiente virtual, instalação das dependências necessárias (LangChain, LangGraph, ChromaDB, HuggingFace) e organização modular dos códigos em src/.

# 🚀 Estrutura do Projeto

A pasta src/ contém os códigos separados por módulos e aulas:

- Módulo 2 – Terminal
- m2aula1: Códigos simples de LangChain e LangGraph
- m2aula2: Códigos com LangChain e LangGraph, aplicando BD Vetorial e recursos
- m2aula3: Códigos com Loaders e ChromaDDB, com recuperação de dados do banco
- m2aula4: Códigos com data ingestion com uso de loaders,retriever e aplicação de QA tanto em Chain quanto em Graph.
- m2aula5: Códigos com personalização das respostas do RAG com parâmetros e prompts.
- Módulo 3 – Streamlit
- m3aula1: **\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***
- m3aula2: **\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***
- m3aula3: **\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***
- m3aula4: **\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***\*\*\*\***

# ⚙️ Configuração do LM Studio

Este projeto utiliza o LM Studio como servidor local de modelos.
No arquivo config.py, estão definidas funções para configurar chamadas tanto via LangChain quanto via cliente OpenAI:

- Base URL: http://127.0.0.1:1234/v1
- API Key: lm-studio
- Modelo: meta-llama-3.1-8b-instruct
  Funções disponíveis:
- get_langchain_model(): retorna o modelo configurado para uso com LangChain.
- get_openai_client(): retorna o cliente OpenAI para chamadas diretas.
  Isso permite alternar facilmente entre chamadas via LangChain e chamadas diretas ao servidor do LM Studio.

# ⚙️ Criando um ambiente

Este projeto deve ser configurado em Python 3.12 para garantir compatibilidade com ChromaDB e LangChain.
Utilize os comandos no terminal, dentro da raiz do projeto para criar o ambiente de acordo com a versão.
caso o ambiente não torne-se ativo, use o comando no terminal: .venv\Scripts\activate

```text
py -3.12 -m venv .venv
```

# 🖥️ Selecionando o interpretador e outras config do VS Code

- Ctrl + Shift + P
- Digite: Python: Select Interpreter
- Escolha o Python dentro de .venv
  Se não for criada automaticamente a pasta .vscode/settings.json, crie manualmente com:

  ```text
  {
    // Interpretador Python (ajuste se mudar o nome da pasta .venv)
    "python.defaultInterpreterPath": ".venv/Scripts/python.exe",

    // Formatação automática ao salvar
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "always"
    },

    // Prettier como formatador padrão global
    "editor.defaultFormatter": "esbenp.prettier-vscode",

    // Configuração específica para Python
    "[python]": {
      "editor.defaultFormatter": "ms-python.black-formatter",
      "editor.formatOnSave": true
    },

    // Configuração específica para JSON
    "[json]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode"
    },

    // Configuração específica para Markdown
    "[markdown]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode"
    },

    // Configuração específica para JavaScript/TypeScript
    "[javascript]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[typescript]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode"
    },

    // Pylance: análise de tipos e auto-import
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.diagnosticMode": "workspace",

    // Linting (Flake8 ativo; pode trocar por Ruff se quiser)
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,

    // Configurações do Prettier
    "prettier.singleQuote": true,
    "prettier.trailingComma": "es5",
    "prettier.printWidth": 88
  }
  ```

# 📂 Estrutura de Pastas

```text
├── src/         # Código principal (módulos e aulas)
├── data/        # PDFs e arquivos de suporte
├── .venv/       # Ambiente virtual
├── .vscode/     # Configurações do VS Code
├── .gitignore
└── README.md    # Documentação
```

# 📦 Instalação das dependências

Atualize o pip e instale as bibliotecas:

```text
- python.exe -m pip install --upgrade pip

- pip list                                  // verificar a lista do pip

**Núcleo do LangChain**
- pip install -U langchain
- pip install -U langchain-community
- pip install -U langchain-core
- pip install -U langchain-openai
- pip install -U langchain-tools            // para decorators tipo @tools
- pip install -U langgraph

**HuggingFace + embeddings (com versões fixadas)**
- pip install "langchain-huggingface==1.2.0"
- pip install "huggingface-hub==0.36.2"
- pip install "transformers==4.57.6"
- pip install "sentence-transformers==4.6.1"      // gerador de embeddings - HuggingFaceEmbeddings

**Banco vetorial Chroma**
- pip install -U chromadb                   // cliente Python do ChromaDB - banco de Dados Vetorial
- pip install -U langchain-chroma           // compatibilidade chroma com langchain

**Utilitários de texto**
- pip install -U langchain-text-splitters   // faz chunks de textos
- pip install -U wikipedia                  // biblioteca que acessa a api do wikipedia

**Leitores de PDF/HTML**
- pip install -U pypdf                      // leitor de pdf
- pip install -U pymupdf                    // leitor de pdf
- pip install -U beautifulsoup4             // leitor de html
- pip install -U lxml                       // leitor de html

**Utilitários gerais**
- pip install -U python-dotenv
- pip install -U requests

***Visualização***
- pip install -U streamlit                  // visual para o chat
- pip install -U rich                       // visual para o terminal

```

# ▶️ Ativando e desativando o ambiente

Utilize os comandos no terminal, dentro da pasta do projeto.

### Ativar

```text
.venv\Scripts\activate
```

### Desativar

```text
deactivate
```

# 📝 Observações

- Para usar modelos HuggingFace sem limite, deve-se configurar um token no site [Link](https://huggingface.co/settings/tokens)
  e no config.py informar diretamente conforme abaixo.

```text
set HF_TOKEN=seu_token_aqui
```
