# Minecraft Vanilla Chatbot

A Minecraft Chatbot in Python which uses a server's log to react to various events (player join/leave, chat) via RCON\
It does not require any plugins (e.g. Spigot) and works in plain vanilla Minecraft


## server.properties
Make sure your server's server.properties file contains the following lines to enable and setup RCON:
```
enable-rcon=true
rcon.port=25575
rcon.password=YOUR-RCON-PASSWORD
```