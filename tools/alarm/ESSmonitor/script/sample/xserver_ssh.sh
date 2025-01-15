
echo -n "k18server pass? : "
read -s ans1
echo ""

echo -n "xserver pass? : "
read -s ans2
echo ""

sshpass -P "Enter passphrase for key" -p $ans2 ssh -i j89k18sks.txt -p 10022 -oProxyCommand='sshpass -p '$ans1' ssh -W %h:%p sks@k18server' j89k18sks@j89k18sks.xsrv.jp
