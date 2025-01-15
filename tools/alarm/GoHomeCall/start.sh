session_name="GoHomeCall"
tmux new-session -d -s ${session_name}
tmux set-option -t ${session_name} set-remain-on-exit on
tmux send-keys -t ${session_name} "./GoHomeCall" C-m
#tmux send-keys -t ${session_name} "./GoHomeCall23" C-m
#tmux a -t ${session_name}
