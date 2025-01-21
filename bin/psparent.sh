#!/usr/bin/env bash
#
# Usage: ./psparent.sh <PID>

# If no PID is provided, show usage and exit.
if [ -z "$1" ]; then
  echo "Usage: $0 <PID>"
  exit 1
fi

pid="$1"

while [[ -n "$pid" && "$pid" -ne 0 ]]; do
  parents+=("$pid")
  # Get the parent PID using ps. '-o ppid=' strips out column headers.
  output=$(ps -o ppid=,cmd= -p "$pid" 2>/dev/null)
  pid=$(echo $output | awk '{print $1}')
  echo $output
done

