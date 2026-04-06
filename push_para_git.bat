@echo off
echo ==================================================
echo        Sincronizador Automatico de Nuvem
echo ==================================================
echo.

set /p mensagem="Digite o que voce fez (ou de ENTER para usar "Atualizacao"): "
if "%mensagem%"=="" set mensagem="Atualizacao do projeto"

echo.
echo Salvando na maquina...
git add .
git commit -m "%mensagem%"

echo.
echo Subindo para o GitHub (Aguarde)...
git push origin main

echo.
echo ==================================================
echo TUDO PRONTO! Seu Github esta atualizado.
echo ==================================================
pause
