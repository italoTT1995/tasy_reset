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

---

## 🤝 Para Novos Desenvolvedores (Onboarding)

Se você acabou de baixar (clonar) este repositório para ajudar no projeto, siga estes passos exatos para subir a máquina na sua casa/empresa:

1. **Baixe o Código:** 
   Clone o repositório (`git clone <url-do-repositorio>`).
2. **Crie o Cofre de Senhas (.env):**
   - O git ignorou as senhas de produção do autor original (por segurança).
   - Você verá um arquivo chamado `.env.example`.
   - Crie uma **cópia** desse arquivo na mesma pasta e renomeie ela para `.env`.
   - Coloque as suas credenciais de ambiente de homologação dentro do seu novo `.env`.
3. **Instale as Máquinas:**
   - Crie a venv rodando `python -m venv .venv`
   - Entre nela rodando `.venv\Scripts\activate` (no Windows)
   - Instale as blibliotecas: `pip install -r requirements.txt`
   - Instale o navegador embutido do Playwright obrigatório: `playwright install chromium`
4. **Modo Visual (Debug):**
   - Se precisar ver o robô trabalhando, abra o arquivo `services/tasy_service.py` e procure a linha onde existe o `headless=False` na chamada base e modifique para true ou vice-versa.
   
---

## 🚀 Como Enviar Atualizações (Para toda a Equipe)

Sempre que você ou seu colega terminarem de escrever um bloco de código novo ou consertarem um bug, sigam este roteiro sagrado para "postar" a atualização no GitHub sem conflitos:

1. **Puxe as novidades (Antes de codar):**
   *Antes de começar o dia de trabalho*, rode isto para garantir que seu computador tem o código que seu colega subiu na noite anterior:
   ```bash
   git pull origin main
   ```

2. **Salve no cofre local (Após codar):**
   ```bash
   git add .
   git commit -m "feat: descricao curta do que foi ajustado ou adicionado"
   ```

3. **Suba para a nuvem do GitHub (Push):**
   ```bash
   git push origin main
   ```
   
> **Dica de ouro:** O arquivo `.env` (onde ficam as senhas do hospital) não sobe para a tela dos colegas pelo push. Ele é travado. Cada um gerencia o seu próprio cofre na sua máquina.

Bem vindo ao projeto!
