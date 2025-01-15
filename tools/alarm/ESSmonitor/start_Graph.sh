session_name="ESS_Graph"
tmux new-session -d -s ${session_name}
tmux set-option -t ${session_name} remain-on-exit on
tmux send-keys -t ${session_name} "cd Monitor" C-m
tmux send-keys -t ${session_name} "./EssMonitor" C-m
#tmux a -t ${session_name
