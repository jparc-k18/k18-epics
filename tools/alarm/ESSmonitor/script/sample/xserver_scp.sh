
echo -n "k18server pass? : "
read -s ans1
echo ""

echo -n "xserver pass? : "
read -s ans2
echo ""


while :
do

date
echo "send file"

sshpass -P "Enter passphrase for key" -p $ans2 scp -p -i j89k18sks.txt -P 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server' ./Monitor/EssHistry.gif j89k18sks@j89k18sks.xsrv.jp:/home/j89k18sks/j89sks.org/public_html/k18/ 2> /dev/null

sshpass -P "Enter passphrase for key" -p $ans2 scp -p -i j89k18sks.txt -P 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server' ../CamCapture2/Monitor/PressHistry.gif j89k18sks@j89k18sks.xsrv.jp:/home/j89k18sks/j89sks.org/public_html/k18/ 2> /dev/null

sshpass -P "Enter passphrase for key" -p $ans2 scp -p -i j89k18sks.txt -P 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server' ../E40H2Tmonitor/E40H2T_labview.jpg j89k18sks@j89k18sks.xsrv.jp:/home/j89k18sks/j89sks.org/public_html/k18/ 2> /dev/null

sshpass -P "Enter passphrase for key" -p $ans2 scp -p -i j89k18sks.txt -P 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server' ../E40H2Tmonitor/E40H2T_labview.jpg j89k18sks@j89k18sks.xsrv.jp:/home/j89k18sks/j89sks.org/public_html/k18/ 2> /dev/null

sshpass -P "Enter passphrase for key" -p $ans2 scp -p -i j89k18sks.txt -P 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server' ../CamCapture_H2/E40H2T_AlertDisp.jpg j89k18sks@j89k18sks.xsrv.jp:/home/j89k18sks/j89sks.org/public_html/k18/ 2> /dev/null

sshpass -P "Enter passphrase for key" -p $ans2 scp -p -i j89k18sks.txt -P 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server' ../CamCapture_H2/E40H2T_camera_6point.jpeg j89k18sks@j89k18sks.xsrv.jp:/home/j89k18sks/j89sks.org/public_html/k18/ 2> /dev/null

sleep 60

done

