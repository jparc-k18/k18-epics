session_name="ESS_SendGarphXserver"
tmux new-session -d -s ${session_name}
tmux set-option -t ${session_name} remain-on-exit on
tmux send-keys -t ${session_name} "./script/sendxserver.sh" C-m
tmux a -t ${session_name}
