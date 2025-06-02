@echo off
REM Muda para o diretório onde este arquivo .bat está localizado
cd /d "%~dp0"

REM Define o nome da pasta do ambiente virtual e o nome do script Python
SET VENV_DIR=myvenv
SET PYTHON_SCRIPT=subscriber.py

REM --- Verificações de Existência (Opcional, mas bom para debug) ---
IF NOT EXIST "%VENV_DIR%\Scripts\Activate.ps1" (
  echo ERRO: Script de ativacao do PowerShell '%VENV_DIR%\Scripts\Activate.ps1' nao encontrado.
  echo Verifique se o nome da pasta do ambiente virtual esta correto e se o .bat esta na pasta raiz do projeto.
  pause
  exit /b
)
IF NOT EXIST "%PYTHON_SCRIPT%" (
  echo ERRO: Script Python '%PYTHON_SCRIPT%' nao encontrado.
  pause
  exit /b
)

REM --- Monta a String de Comandos para o PowerShell ---
REM Usamos o ponto e vírgula (;) para separar múltiplos comandos no PowerShell.
REM O comando 'Read-Host' no final age como um "pause" personalizado no PowerShell.
SET "POWER_COMMANDS=Write-Host '--- Iniciando execucao no PowerShell ---'; Write-Host 'Ativando ambiente virtual: %VENV_DIR% ...'; .\%VENV_DIR%\Scripts\Activate.ps1; Write-Host 'Ambiente virtual ativado (verifique o prompt).'; Write-Host 'Executando script Python: %PYTHON_SCRIPT% ...'; python .\%PYTHON_SCRIPT%; Write-Host ''; Write-Host '--- Script Python finalizado ---'"

REM --- Executa o PowerShell ---
echo Abrindo PowerShell e executando os comandos...
REM -ExecutionPolicy Bypass: Permite rodar o Activate.ps1 sem alterar a política global.
REM -NoExit: Mantém a janela do PowerShell aberta após os comandos terminarem.
REM -Command "& { ... }": Executa o bloco de script fornecido.
powershell.exe -ExecutionPolicy Bypass -NoExit -Command "& { %POWER_COMMANDS%; Write-Host ''; Read-Host 'Pressione ENTER para fechar esta janela do PowerShell.' }"

echo.
echo O script .bat terminou. A execucao continua na janela do PowerShell.