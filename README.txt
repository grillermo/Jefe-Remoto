Jefe Remoto
It's my little itch i had to scratch.

What itch was i scratching?
I wanted to send and execute files remotely to administer computers but the current solutions are huge and overblown like Active Directory and i want it to be dead simple, you run a simple file on the computers you want to send files to execute and then with a drag and drop you are sending them files. That simple.

Purpose:
To automate the transfering of file to multiple computers with the least number of clicks posible for the purpose of simple transfer or executing that file.

Strategy
Python 2.6.6 installes on all the machines
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