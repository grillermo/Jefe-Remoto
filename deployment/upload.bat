echo Usage
echo argv1: usuario
echo argv2: password
echo argv3: computerlist.txt 
echo argv4: local file
echo argv5: the sentence to execute on the remote machine
echo e.g. upload.bat juan juan list.txt list.txt

psexec.exe @%~3 -u %~1 -p %~2 -c -f -d %~4
