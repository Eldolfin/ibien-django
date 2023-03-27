#!/usr/bin/bash
tmux new-session -s "web" ./manage-prod.sh runserver
