# Modela Sistemas de Transmissão (`EnlineDevEng`)

Guia de instalação e execução do teste da biblioteca.

---

## Etapa 1: Criar a pasta do projeto

Abra o terminal (PowerShell no Windows ou Terminal no Linux/macOS) e execute os comandos abaixo para criar e entrar na pasta onde você fará o teste:

```bash
mkdir test_enlinedeveng
cd test_enlinedeveng
```

---

## Etapa 2: Criar e ativar o ambiente virtual

Crie o ambiente virtual isolado dentro da pasta:

```bash
python -m venv .venv
```

Ative o ambiente virtual executando o comando correspondente ao seu sistema:

* **Windows (PowerShell):**

  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

  *(Se o PowerShell bloquear a execução, rode o comando abaixo e depois repita o comando de ativação acima)*:

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
* **Windows (Prompt de Comando / CMD):**

  ```cmd
  .venv\Scripts\activate.bat
  ```
* **Linux / macOS:**

  ```bash
  source .venv/bin/activate
  ```

> Confirme que `(.venv)` apareceu no início da linha do terminal antes de seguir.

---

## Etapa 3: Instalar a biblioteca via `pip`

Com o `(.venv)` ativo, execute o comando de instalação diretamente do GitHub:

* **Via HTTPS (pede usuário e token do GitHub):**

  ```bash
  pip install "git+https://github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git#subdirectory=enlinedeveng"
  ```
* **Via SSH (para quem usa chave SSH configurada no GitHub):**

  ```bash
  pip install "git+ssh://git@github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git#subdirectory=enlinedeveng"
  ```


---

## Etapa 4: Baixar os arquivos de exemplo e abrir o VS Code

1. Baixe a pasta `tests/` deste repositório (contendo o notebook de teste e os arquivos `.pwf` de exemplo) e coloque dentro da pasta `test_enlinedeveng`. Esta pasta 'tests/' está neste caminho: 'teste_enlinedeveng\.venv\Lib\site-packages\EnlineDevEng\tests' ou se preferir pode
   baixá-la diretamente do repositório do caminho: 'EnlineDevEng/tests'
2. Ainda no terminal, com `(.venv)` ativo, abra o VS Code na pasta atual:

```bash
code .
```

---

## Etapa 5: Executar o teste no VS Code


### Executando pelo terminal (`.py`)

Abra o terminal do VS Code (`Ctrl + '`), garanta que `(.venv)` está ativo e execute:

```bash
python tests/main.py
```

---

## Como atualizar para versões futuras

Quando houver atualizações no repositório, ative o `(.venv)` da sua pasta e execute:

```bash
pip install --upgrade --force-reinstall "git+https://github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git#subdirectory=enlinedeveng"
```
