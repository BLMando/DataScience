#!/bin/bash

tmux new-session -d -s rasa-session
tmux send-keys -t rasa-session 'source avenv rasa && rasa run --enable-api --cors "*" --debug' C-m
tmux split-window -h
tmux send-keys -t rasa-session 'source avenv rasa && rasa run actions' C-m
tmux split-window -v
tmux send-keys -t rasa-session 'ngrok http 5005' C-m

tmux attach-session -t rasa-session
