# gas check
session_name="GasCheckCall"
tmux new-session -d -s ${session_name}
#tmux set-option -t ${session_name} set-remain-on-exit on
tmux send-keys -t ${session_name} "./call_gascheck.py $1" C-m

# isob check
session_name="IsobCheckCall"
tmux new-session -d -s ${session_name}
tmux send-keys -t ${session_name} "./call_isobcheck.py $1" C-m
#tmux a -t ${session_name}
