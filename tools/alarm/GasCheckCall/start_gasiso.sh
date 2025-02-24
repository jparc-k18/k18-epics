# gasiso check
session_name="GasIsoCheckCall"
tmux new-session -d -s ${session_name}
#tmux set-option -t ${session_name} set-remain-on-exit on
tmux send-keys -t ${session_name} "./auto_call_gasisocheck.py $1" C-m
