#!/bin/bash
git add -A
git commit -m '$1'
git push
ssh awt "cd /opt/awt/slidesyncshare && git pull && docker-compose up -d --force-recreate;"
