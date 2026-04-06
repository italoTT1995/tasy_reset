# Tasy EMR - Reset Automático de Senhas

Ferramenta CLI para automação avançada de redefinição de senhas com Playwright construída com alta resiliência para interfaces Single Page Application (AngularJS).

## Setup Local

1. Crie o ambiente virtual (Recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Instale as dependências requisitadas:
   ```bash
   pip install -r requirements.txt
   ```
3. Instale os navegadores do Playwright:
   ```bash
   playwright install chromium
   ```
4. Configure as variáveis de ambiente:
   Abra o arquivo `.env` na raiz do projeto e ajuste suas variáveis de login seguro.
   ```
   TASY_URL=https://exemplo...
   ADMIN_USER=admin
   ADMIN_PASSWORD=admin
   ```

## Módulo de Execução

Rodar através do CLI com os argumentos:

```bash
python main.py --usuario "hcucandido" --nova_senha "SenhaSegura123"
```

## Logs e Debug
O robô cria uma pasta chamada `logs` gerando rastreamentos diários em arquivos rotativos automaticamente. Se um erro crítico acontecer, ele salva a tela atual na pasta `screenshots` para debug assíncrono.
