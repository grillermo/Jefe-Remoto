echo Usage
echo argv1: usuario
echo argv2: password
echo argv3: computerlist.txt 
echo argv4: local file
echo argv5: the sentence to execute on the remote machine
echo e.g. uploadandexecute.bat juan juan list.txt python-3.2.msi "msiexec /i python-3.2.msi TARGETDIR=C:\JefeRemoto\Python32 ALLUSERS=1 /qn"

psexec.exe @%~3 -u %~1 -p %~2 -c -f -d %~4
PAUSE
echo
echo
psexec.exe @%~3 -u %~1 -p %~2 -i %~5