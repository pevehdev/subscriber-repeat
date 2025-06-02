# Script de Inscrição Automática em Torneios Repeat.gg (Fortnite)

Este script Python utiliza Selenium para automatizar o processo de encontrar e se inscrever em torneios "Entrada Livre" de Fortnite no site Repeat.gg. Ele também inclui uma etapa inicial interativa para facilitar o login do usuário se a sessão não estiver ativa.

## Funcionalidades Principais

* Abre o Google Chrome utilizando uma cópia isolada de um perfil de usuário.
* Na primeira execução (se não estiver logado):
    * Navega para o site Repeat.gg.
    * Tenta clicar no pop-up de consentimento de cookies.
    * Verifica se o usuário está logado.
    * Se não estiver logado, pausa e instrui o usuário a fazer login manualmente na janela do navegador aberta.
    * Após o login manual, o script é encerrado para que o usuário o execute novamente (o login ficará salvo no perfil copiado).
* Em execuções subsequentes (com o perfil já logado):
    * Navega até a página de torneios de Fortnite do Repeat.gg.
    * Identifica todos os torneios marcados como "Entrada Livre" que não estão "Fechados".
    * Para cada torneio elegível:
        * Navega para a página de detalhes do torneio.
        * Localiza e clica no botão "Junte-se ao torneio".
    * Processa todos os torneios elegíveis encontrados.

## Pré-requisitos

* Python 3.7 ou superior.
* PIP (gerenciador de pacotes Python).
* Navegador Google Chrome instalado.

## Configuração do Ambiente

Siga estes passos para configurar o ambiente e o script:

**1. Clone ou Faça o Download do Script**
    * Salve o arquivo Python (`subscriber.py`) na pasta do seu projeto.
    * Crie um arquivo chamado `requirements.txt` na mesma pasta com o seguinte conteúdo:
        ```
        selenium
        webdriver-manager
        ```

**2. Crie um Ambiente Virtual (Recomendado)**
    Abra o terminal ou PowerShell na pasta do seu projeto e execute:
    ```bash
    python -m venv myvenv
    ```
    Para ativar o ambiente virtual:
    * Windows (PowerShell): `.\myvenv\Scripts\Activate.ps1`
    * Windows (CMD): `myvenv\Scripts\activate.bat`
    * macOS/Linux: `source myvenv/bin/activate`

    *Nota sobre PowerShell no Windows:* Se você receber um erro sobre a execução de scripts estar desabilitada (`PSSecurityException`), pode ser necessário executar o seguinte comando em um PowerShell aberto como Administrador:
    `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
    E confirme com `S` ou `A`.

**3. Instale as Dependências Python**
    Com o ambiente virtual ativado, instale as dependências listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    Se você preferir gerar o `requirements.txt` com as versões exatas após instalar manualmente (`pip install selenium webdriver-manager`), você pode usar (com o ambiente virtual ativado):
    ```bash
    python -m pip freeze > requirements.txt
    ```

**4. Configure o Perfil do Google Chrome (Passo CRUCIAL)**
    Para que o script salve seu login do Repeat.gg de forma persistente entre as execuções, ele utiliza uma cópia isolada de um perfil do Chrome.

    * **a. Crie um Novo Perfil no Chrome (se ainda não tiver um dedicado para o bot):**
        * Abra o Google Chrome manualmente.
        * Clique no ícone do seu perfil atual (canto superior direito) > "Adicionar" (ou "Gerenciar Perfis" > "Adicionar perfil").
        * Dê um nome ao novo perfil (ex: "RepeatBotProfile") e finalize a criação.

    * **b. (Opcional - para a primeira execução do script) Faça Login no Repeat.gg neste Novo Perfil:**
        * Na janela do Chrome que abriu com o novo perfil ("RepeatBotProfile"), navegue até `https://www.repeat.gg/` e faça login manually com sua conta do Repeat.gg. Marque "Lembrar-me" se disponível. *Alternativamente, o script guiará você por este login na primeira vez que rodar.*

    * **c. Feche o Chrome:** Feche todas as janelas do Google Chrome, especialmente as que estiverem usando este novo perfil "RepeatBotProfile".

    * **d. Localize a Pasta do Novo Perfil:**
        * Reabra o Chrome e selecione o novo perfil "RepeatBotProfile".
        * Na barra de endereços, digite `chrome://version` e pressione Enter.
        * Copie o valor do campo **"Caminho do perfil"**. Será algo como `C:\Users\<SeuNomeDeUsuario>\AppData\Local\Google\Chrome\User Data\Profile X` (onde `X` é um número, como `Profile 3`).

    * **e. Crie a Pasta para a Cópia Isolada do Perfil:**
        * Crie uma nova pasta vazia no seu computador. O script atual está configurado para usar `C:\TempChromeSeleniumProfile`. Se você usar um caminho diferente, precisará atualizar o script.
            ```
            # Pasta usada no script:
            C:\TempChromeSeleniumProfile
            ```
        * Certifique-se de que esta pasta (`C:\TempChromeSeleniumProfile`) esteja vazia antes do próximo passo.

    * **f. Copie o Conteúdo do Perfil para a Pasta Isolada:**
        * **Com TODAS as instâncias do Chrome FECHADAS (verifique o Gerenciador de Tarefas por `chrome.exe`)**, copie todo o conteúdo da pasta que você identificou no "Caminho do perfil" (ex: de `...\User Data\Profile 3`) para dentro da pasta `C:\TempChromeSeleniumProfile`.

    * **g. Verifique o Script Python (`subscriber.py`):**
        Confirme se a variável `profile_user_data_dir` no script Python está apontando para a pasta da cópia isolada:
        ```python
        # No script subscriber.py:
        profile_user_data_dir = r"C:\TempChromeSeleniumProfile" 
        ```

**5. Configure o Script (`subscriber.py` - se necessário)**
    * Verifique se a variável `fortnite_tournaments_url` no script está correta (`https://www.repeat.gg/pc/fortnite`).
    * Os seletores XPath para os elementos da página podem precisar de ajuste se o site Repeat.gg mudar sua estrutura HTML no futuro.

## Como Executar o Script

1.  **Primeira Execução (para configurar o login no perfil do script):**
    * Certifique-se de que a pasta do perfil copiado (ex: `C:\TempChromeSeleniumProfile`) exista.
    * Ative seu ambiente virtual.
    * Execute o script: `python subscriber.py`
    * O script abrirá o navegador. Se detectar que você não está logado no Repeat.gg, ele pausará e pedirá para você fazer login manualmente na janela do navegador.
    * Após fazer login no navegador, volte ao console e pressione Enter.
    * O script informará que será encerrado e fechará o navegador. O login agora estará salvo na pasta `C:\TempChromeSeleniumProfile`.

2.  **Execuções Subsequentes:**
    * Ative seu ambiente virtual.
    * Execute o script: `python subscriber.py`
    * O script agora deve detectar que você já está logado (usando os cookies salvos no perfil `C:\TempChromeSeleniumProfile`) e prosseguirá diretamente para a lógica de encontrar e se inscrever nos torneios.

## Funcionamento Esperado (Após Login Configurado)

Ao ser executado:
1.  Inicia uma instância do Chrome usando a cópia do perfil (`C:\TempChromeSeleniumProfile`).
2.  Verifica o estado do login. Se logado, prossegue.
3.  Navega para a página de torneios do Fortnite no Repeat.gg.
4.  Identifica torneios "Entrada Livre" que não estão "Fechados".
5.  Para cada torneio encontrado:
    * Abre a página de detalhes do torneio.
    * Localiza e clica no botão "Junte-se ao torneio".
    * Imprime mensagens no console sobre o progresso.
6.  Fecha o navegador ao final.

## Possíveis Problemas e Observações

* **Script Não Encontra Elementos:** Se o Repeat.gg atualizar o design do site, os seletores XPath podem quebrar.
* **Classes `mui-xxxxx`:** Classes geradas automaticamente podem ser instáveis.
* **Bloqueios ou CAPTCHAs:** O site pode detectar automação. Pausas (`time.sleep()`) ajudam, mas não são garantia.
* **Termos de Serviço:** Respeite os Termos de Serviço do Repeat.gg. O uso de scripts é por sua conta e risco.