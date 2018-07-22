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
    print("-debug_song to print debug statements in song creator")
    print "-debug_dmxd to print debug statements in dmxd.o when it runs"
    
    print "-bpm (number) to set static bpm"
    print "\n"
    exit()

try:
    #ssh
    t = paramiko.client.SSHClient()
    t.set_missing_host_key_policy(paramiko.client.WarningPolicy)
    t.connect(
            #set_missing_host_key_policy=False,
            hostname=hostname,
            port=port,
            username=username,
            look_for_keys=False,
            password=password
        )
    tsftp=t.open_sftp()
    
    args_as_string = " ".join(argv[1:])   
    
    #recompile song
    if "-drc" in argv:
        print "not recompiling song"
    else:
        cmd = "sudo python {}/play_songs/src/songCreator.py {}".format(source, args_as_string)
        call(cmd.split())
    


    print("")

    #recompile dmxd.o (on pi):
    if "-dm" in argv:
        print("not remaking dmxd.o")
    else:
        tsftp.put(
            source + "/play_songs/src/dmxd.c",
            dest + "/play_songs/src/dmxd.c"
        )
        cmd = "make -C {}/play_songs/src/".format(dest) 
        print(cmd)
        stdin, stdout, stderr = t.exec_command(cmd)
        if(stderr):
            print("STDERR:")
            print("".join(stderr.readlines()))
        print("STDOUT:")
        print("".join(stdout.readlines()))
        print("finished making dmxd.c successfully")

except Exception as e:
    print(sys.exc_info())

finally:
    t.close()
