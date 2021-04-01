#!/bin/bash
catkin_make
source devel/setup.bash
if [[ "$(xprop -id "$(xdotool getactivewindow)" WM_CLASS)" == *"gnome-terminal"* ]]; then
  sleep 0.1
  xdotool key ctrl+shift+t
  gnome-terminal -e "bash -c 'roscore'"
  

elif ! pgrep 'gnome-terminal'; then
  gnome-terminal
fi

if [[ "$(xprop -id "$(xdotool getactivewindow)" WM_CLASS)" == *"gnome-terminal"* ]]; then
  sleep 0.1
  xdotool key ctrl+shift+t
  gnome-terminal -e "bash -c 'rosrun dynamixel_sdk_examples read_write_node'"
  

elif ! pgrep 'gnome-terminal'; then
  gnome-terminal
fi

