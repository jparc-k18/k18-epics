session_name="ShiftChangeCall"
tmux new-session -d -s ${session_name}
tmux set-option -t ${session_name} set-remain-on-exit on
tmux send-keys -t ${session_name} "./ShiftChangeCall" C-m
#tmux a -t ${session_name}
