screen -d -m -S test /dev/ttyACM0 115200
input="/home/pi/AAHH/Songs/$1/compiled_song"
tempo=0
screen -S test -X stuff "echo r"
echo "${input:0:1}"
while IFS= read -r line
do
  if [ "${line:0:1}" = '-' ]
  then
    tempo=${line:1}
    echo "$tempo"
  else
  echo "$line"
    screen -S test -X stuff "echo '$line'"
    sleep $tempo
  fi
done < "$input"
screen -S test -X stuff "echo r"


