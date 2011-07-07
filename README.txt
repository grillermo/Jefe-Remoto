Jefe Remoto
It's my little itch i had to scratch.

Screenshots
http://dl.dropbox.com/u/1729028/client%20view.png
http://dl.dropbox.com/u/1729028/server%20view.png

What itch was i scratching?
I wanted to send and execute files remotely to administer computers but the current solutions are huge and overblown like Active Directory and i want it to be dead simple, you run a simple file on the computers you want to send files to execute and then with a drag and drop you are sending them files. That simple.

Third parties:
PyQt4 http://www.riverbankcomputing.co.uk/software/pyqt/download
ConfigObj http://www.voidspace.org.uk/python/configobj.html
PypMsg 0.2 http://pypmsg.blogspot.com/
a pure Python Ping ftp://ftp.visi.com/users/mdc/ping.py

Purpose:
To automate the transfering of file to multiple computers with the least number of clicks posible for the purpose of simple transfer or executing that file.

Strategy
Simple client-server

Python 2.6.6 installed on all the machines.
First you get your server wich can generate a ftpserver.py(on the future native executables).
On the client side you get an fptserver.py pre-configured with the user,password and server to connect to.
On this client i also have a small socket messaging communication to broadcast to the server our status.
The server then creates a list of computers we can send files to.
And then we simply drag and drop a file to our nice server GUI and then we hit send and off the file goes sequencially to all the computers on the list.
The client gets the file(tested with files up to 3.5 gbs) and sees if its extension its .exe .py .skl .ahk .msi and if it is, it runs the file.

ROADMAP:
-Encryption: this is a big one, right now communications are unencrypted between the clients and the server.
-Multiple files: a no brainer.
-Since i got a complete ftp server running on my clients i want to be able to read a report file or maybe clean the drop folder.
-Linux and OSX, the infrastructure is there i will eventually port both the client and the server to run on both platforms(python it's awesome for this)
-.exe .app .deb creation by our server gui, i tried this with pyinstaller but and it kind of worked on Windows, this will happen for the 3 platforms.

Sorries:
I only got a few months programming in python so i still got a lot of work to do, i'm refactoring the code right now to look better but i think the basic functionallity is there.

You want to help
I'm really struggling with writting a complete ssh server in python i tried a few googled ones but i couldn't get them to work i'd love to hear from you if you have even a simple solution i can work with.

Licence
'''
   Copyright 2011 Guillermo Siliceo Trueba

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
Contact me @grillermo on twitter
