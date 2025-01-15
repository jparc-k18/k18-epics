
echo -n "pass? : "
read -s ans
echo ""

while :
do

echo "send file"
#sshpass -p $ans scp -o StrictHostKeyChecking=no cap_sdc23_cam.jpg sks@k18server.intra.j-parc.jp:~/html/e40/SDC23press_light/

#cp Monitor/PressHistry.gif ~/Dropbox/SDC23/
#cp Monitor/EssHistry.gif /mnt/sdb1/dropbox/Dropbox/SDC23/


sleep 60

done
