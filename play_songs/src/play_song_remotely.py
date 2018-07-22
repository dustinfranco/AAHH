from subprocess import call
from os import environ
from sys import argv
import paramiko

hostname = environ["PI_HOSTNAME"]
username = environ["PI_USERNAME"]
password = environ["PI_PASSWORD"]
source = environ["LOCAL_AAHH"]
dest = environ["PI_AAHH"]
port = int(environ["PI_PORT"])
if len(argv) < 2:
    print("need to pass in an argument, 'h' for help")
    exit()

if(argv[1][0] == "h"):
    print "\n"
    print "HOW TO USE PLAY REMOTELY:"
    print "first argument should be song name"
    print "-dm to disable 'remake dmxd.o and scp it'"
    print "-drc to disable recompiling the song"
    print "-dhw to disable hardware optimization"
    print "-debug to print debug statements in dmxd.o when it runs"
    print "-bpm (number) to set static bpm"
    print "\n"
    exit()

try:
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(source, dest)

except Exception as e:
    print(e)

finally:
    t.close()
