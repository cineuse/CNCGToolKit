@echo off
rem cd to here
E:
cd %~dp0
echo %cd%
pyside-rcc -o icons_rc.py icons.qrc 
pyside-rcc -o other_images_rc.py other_images.qrc 
pyside-rcc -o cg_apps_rc.py cg_apps.qrc 
pause