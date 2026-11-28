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

- **Windows (PowerShell):**

  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

  *(Se o PowerShell bloquear a execução, rode o comando abaixo e depois repita o comando de ativação acima)*:

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

- **Windows (Prompt de Comando / CMD):**

  ```cmd
  .venv\Scripts\activate.bat
  ```

- **Linux / macOS:**

  ```bash
  source .venv/bin/activate
  ```

> Confirme que `(.venv)` apareceu no início da linha do terminal antes de seguir.

---

## Etapa 3: Instalar a biblioteca via `pip`

Com o `(.venv)` ativo, execute o comando de instalação diretamente do GitHub:

- **Via HTTPS (recomendado para repositório público):**

  ```bash
  pip install "git+[https://github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git#subdirectory=EnlineDevEng](https://github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git#subdirectory=EnlineDevEng)"
  ```

- **Via SSH (para quem usa chave SSH configurada no GitHub):**

  ```bash
  pip install "git+ssh://git@github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git#subdirectory=EnlineDevEng"
  ```

---

## Etapa 4: Baixar apenas a pasta `tests/` e abrir o VS Code

1. Ainda dentro de `test_enlinedeveng`, execute os comandos abaixo para baixar somente a pasta `tests/` do repositório:

   ```bash
   git clone --filter=blob:none --no-checkout [https://github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git](https://github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git) temp_repo
   cd temp_repo
   git sparse-checkout set tests
   git checkout main
   ```

2. Mova a pasta `tests/` para a raiz de `test_enlinedeveng` e remova a pasta temporária:

   - **Windows (PowerShell):**
     ```powershell
     Move-Item -Path .\tests -Destination ..\tests
     cd ..
     Remove-Item -Recurse -Force .\temp_repo
     ```

   - **Windows (Prompt de Comando / CMD):**
     ```cmd
     move tests ..\tests
     cd ..
     rmdir /s /q temp_repo
     ```

   - **Linux / macOS:**
     ```bash
     mv tests ../tests
     cd ..
     rm -rf temp_repo
     ```

3. Com `(.venv)` ativo e a pasta `tests/` dentro de `test_enlinedeveng`, abra o VS Code:

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
pip install --upgrade --force-reinstall "git+[https://github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git#subdirectory=EnlineDevEng](https://github.com/Iuri-crypto/Modela_Sistemas_de_Transmissao.git#subdirectory=EnlineDevEng)"
```