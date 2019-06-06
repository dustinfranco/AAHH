local_song="/Users/dustinfranco/projects/AAHH/Songs/$1"
target_song="/home/pi/AAHH/Songs/$1"
sudo python /Users/dustinfranco/projects/AAHH/serial_controller/song_maker/compile_song.py $1
#target_song="/home/pi/AAHH/Songs"
#ssh pi@192.168.42.25 "sudo mkdir '$target_song'"
sudo scp $local_song/compiled_song pi@192.168.42.25:$target_song/compiled_song
sudo ssh pi@192.168.42.25 "bash /home/pi/AAHH/serial_controller/play_song/play_song_local.sh $1"

