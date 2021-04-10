@echo off
set /p commit_text="commit text: "

IF "%commit_text%" == "" (
	for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
)
IF "%commit_text%" == "" (
	set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
)
IF "%commit_text%" == "" (
	set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
)
IF "%commit_text%" == "" (
	set "commit_text=fastPush-%ComputerName%-%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"
)


echo commit message is %commit_text%

echo ========== git ==========
@echo on
git status
git add .
git status
git commit -m "%commit_text%"
git push origin master
git push esat master

pause




