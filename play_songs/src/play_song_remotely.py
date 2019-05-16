from subprocess import call
from os import environ
from sys import argv
import config as cf
import sys
import paramiko
print("environment variables:")
print environ
hostname = cf.piip
username = cf.username
password = cf.pipw
source = cf.local_AAHH
dest = cf.pi_AAHH
port = int(cf.pi_port)

def remote_command(ssh, cmd, blocking = True):
    print("remote exec: {}".format(cmd))
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.channel.recv_exit_status()


    if(stderr):
        print("STDERR:")
        print("".join(stderr.readlines()))
    print("STDOUT:")
    print("".join(stdout.readlines()))


if len(argv) < 2:
    print("need to pass in an argument, 'h' for help")
    exit()

if(argv[1][0] == "h"):
    print "\n"
    #implemented:
    print "HOW TO USE PLAY REMOTELY:"
    print "first argument should be song name"
    print "-dm to disable 'remake local dmxd.bin on pi"
    print "-drc to disable recompiling the song"
    print("-debug_song to print debug statements in song creator")

    #not implemented:
    print "-dhw to disable hardware optimization"
    print "-debug_dmxd to print debug statements in dmxd.bin when it runs"
    print "-bpm (number) to set static bpm"
    print "-ps to print song"
    print "\n"
    exit()


try:
    songname = argv[1]
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
    print "copying song to pi"
    tsftp.put(
        "{}/Songs/{}/compiledSections/temp".format(source,songname),
        "{}/Songs/{}/compiledSections/temp".format(dest,songname)
    )
    print "song copied to pi successfully"
    print("")

    #recompile dmxd.o (on pi):
    if "-dm" in argv:
        print("not remaking dmxd.bin")
    else:
        tsftp.put(
            source + "/play_songs/src/dmxd.c",
            dest + "/play_songs/src/dmxd.c"
        )
        cmd = "make -C {}/play_songs/src/".format(dest) 
        remote_command(t, cmd)
    
    #play the song:
    cmd = "sudo {}play_songs/daemon/dmxd.bin {}Songs/{}/compiledSections/temp 120.0".format(dest,dest,songname) 
    remote_command(t, cmd)


except Exception as e:
    print(sys.exc_info())

finally:
    t.close()
