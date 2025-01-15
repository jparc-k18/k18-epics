#echo -n "k18server pass? : "
echo -n "k18server2 pass? : "
read -s ans1
echo ""

echo -n "xserver pass? : "
read -s ans2
echo ""


while :
do

date
echo "send file"

#sshpass -P "Enter passphrase for key" -p $ans2 scp -p -i ./script/j89k18sks.txt -P 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server' ./Monitor/EssHistry.gif j89k18sks@j89k18sks.xsrv.jp:/home/j89k18sks/j89sks.org/public_html/k18/EssHistry.gif 2> /dev/null

sshpass -P "Enter passphrase for key" -p $ans2 scp -p -i ./script/j89k18sks.txt -P 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server2' ./Monitor/EssHistry.gif j89k18sks@j89k18sks.xsrv.jp:/home/j89k18sks/j89sks.org/public_html/k18/EssHistry.gif 2> /dev/null

sleep 60

done
