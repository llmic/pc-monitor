@echo off
:loop
    git add index.html
    git commit -m "Auto update: %date% %time%"
    git push origin master
    timeout /t 90 /nobreak >nul
goto loop