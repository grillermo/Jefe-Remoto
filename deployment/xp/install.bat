cd %SYSTEMDRIVE%
SET INSTALLDIR=C:\Jefe Remoto\

REM #instalando silenciosamente Python en carpeta personalizada
msiexec /i python-2.7.1.msi TARGETDIR="%INSTALLDIR%Python27" /qno
REM #Creamos directorio para herramientas adicionales
mkdir "%INSTALLDIR%\Tools"
REM #Copiando herramientas adicionales
copy setx.exe "%INSTALLDIR%\Tools"
copy XCACLS.vbs "%INSTALLDIR%\Tools"
copy 7z.exe "%INSTALLDIR%\Tools"
REM #Variable de entorno de sistema para python
setx.exe PATH "%PATH%;"%INSTALLDIR%\Python27" -m
REM #Variable de entorno para las herramientas adicionales
setx.exe PATH "%PATH%;"%INSTALLDIR%\Tools" -m
REM #Cambiando contraseña de usuario
net user UsuarioRemoto y59tyi0ZSprlCllV1FTf
REM #Moviendo el usuario al grupo administradores
net localgroup Administradores /add UsuarioRemoto
REM Abriendo puertos para compartir archivos
netsh firewall set service type = fileandprint mode = enable
REM habilitando modo simple de compartir archivos con entrada de registro
regedit.exe /s rules.reg

REM #Copiando el servidor ftp

REM xcopy filezilla-server "c:\Archivos de Programa/pyMassFTP" /s /e