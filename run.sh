#!/bin/bash

# Array of commands to run in different tabs
commands=(
    ' export FLASK_APP=web; flask run -p 5000;'
    ' export FLASK_APP=web; flask run -p 5001;'
    ' export FLASK_APP=web; flask run -p 5002;'
    ' export FLASK_APP=web; flask run -p 5003;'
    ' export FLASK_APP=web; flask run -p 5004;'
    ' export FLASK_APP=web; flask run -p 5005;'
)

# Build final command with all the tabs to launch
set finalCommand=""
for (( i = 0; i < ${#commands[@]} ; i++ )); do
    export finalCommand+="--tab -e 'bash -c \"${commands[$i]}\"' "
done

# Run the final command
eval "gnome-terminal "$finalCommand