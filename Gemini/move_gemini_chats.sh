#!/bin/zsh

mkdir -p /Users/lucasbuetje/gemini_chats
setopt +o nomatch
mv /Users/lucasbuetje/Downloads/gemini-conversation-* /Users/lucasbuetje/gemini_chats/ 2>/dev/null || true
