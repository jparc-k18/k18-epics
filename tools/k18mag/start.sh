# monitor k18d4 and calculate beam momentum
session_name="monitork18mag"
tmux new-session -d -s ${session_name}
#tmux set-option -t ${session_name} set-remain-on-exit on
tmux send-keys -t ${session_name} "./monitork18mag.py $1" C-m
tmux a -t ${session_name}
