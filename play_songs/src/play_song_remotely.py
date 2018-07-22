from subprocess import call
from os import environ
from sys import argv
import sys
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

t=None
if(True):
#try:
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)

    #all arguments as a single string with space delimiter:
    args_as_string = " ".join(argv[1:])   
    #recompile song
    cmd = "sudo python {}/play_songs/src/songCreator.py {}".format(source, args_as_string)
    #call(cmd.split())
    #recompile dmxd.o
    cmd = "sudo make -C {}/play_songs/src/".format(source)
    print(cmd)
    call(cmd.split())
    
    #sftp.put(source, dest)
"""
except Exception as e:
    print(sys.exc_info())

finally:
    t.close()
"""
t.close()
