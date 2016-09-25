echo off
rem get mod template file
set mod_temp_path= %cd%\templates\CNCGToolKit_TEMP.mod
set mod_copy_path= %USERPROFILE%\Documents\maya\modules\CNCGToolKit.mod

rem copy template file
XCopy %mod_temp_path% %mod_copy_path%*

rem replace {ROOT_DIR} by current path
call :FindReplace "{ROOT_DIR}" %cd% %mod_copy_path%

rem functions
:FindReplace <findstr> <replstr> <file>
set tmp="%temp%\tmp.txt"
If not exist %temp%\_.vbs call :MakeReplace
for /f "tokens=*" %%a in ('dir "%3" /s /b /a-d /on') do (
  for /f "usebackq" %%b in (`Findstr /mic:"%~1" "%%a"`) do (
    echo(&Echo Replacing "%~1" with "%~2" in file %%~nxa
    <%%a cscript //nologo %temp%\_.vbs "%~1" "%~2">%tmp%
    if exist %tmp% move /Y %tmp% "%%~dpnxa">nul
  )
)
del %temp%\_.vbs
exit /b

:MakeReplace
>%temp%\_.vbs echo with Wscript
>>%temp%\_.vbs echo set args=.arguments
>>%temp%\_.vbs echo .StdOut.Write _
>>%temp%\_.vbs echo Replace(.StdIn.ReadAll,args(0),args(1),1,-1,1)
>>%temp%\_.vbs echo end with