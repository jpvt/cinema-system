#!/bin/bash

# Setup DEV Application
# João Pedro Vasconcelos - jpvteixeira99@gmail.com
# First Version: 2022-11-30

# colors
NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

echo -e ""
echo -e "⚙️  DEV Application Setup"
echo -e ""
echo -e "➡️  This build takes ~ Y seconds on a 150Mbps connection"
echo -e "➡️  and stores ~ Z MB of data on your disk."
echo -e ""

# deploying locally
echo -e ""
echo -e "⚙️  Starting app environment with docker compose..."
docker compose up -d
if [ "$?" -ne 0 ]; then
    echo -e ""
    echo -e "${RED}Error deploying the environment. Run $0 again.${NC} ❌"
    exit 1
else
    echo -e "${GREEN}Done!${NC} ✅"
fi

echo -e ""
echo -e "⚙️  Wait a few seconds while the application is being deployed..."
count=1
while true; do
   curl http://localhost:8501
   if [ "$?" -ne 0 ]; then
      sleep 45
   else
      break
   fi
   if [ $count -eq 5 ]; then
      echo -e ""
      echo -e "${RED}Timeout. Run $0 again.${NC} ❌"
      docker compose down
      exit 1
   fi
   count=$(($count+1))
done


echo -e ""
echo -e "💻 Your Application is finished! ✅"
echo -e ""
