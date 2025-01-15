session_name="ESS_ReadCycle"
tmux new-session -d -s ${session_name}
tmux set-option -t ${session_name} remain-on-exit on
tmux send-keys -t ${session_name} "./HtmlESS 50" C-m
#tmux a -t ${session_name}
