#!/bin/bash
# Quick Push - Simple wrapper for common commits
# Usage: ./quick_push.sh [message]

if [ -z "$1" ]; then
    ./auto_push_to_github.sh
else
    ./auto_push_to_github.sh "$1"
fi
