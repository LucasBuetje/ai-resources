#!/bin/zsh

mkdir -p "$HOME/gemini_chats"
setopt +o nomatch
mv "$HOME"/Downloads/gemini-conversation-* "$HOME/gemini_chats/" 2>/dev/null || true
