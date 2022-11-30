#!/bin/bash

# Setup DEV Environment
# João Pedro Vasconcelos - jpvteixeira99@gmail.com
# First Version: 2022-11-30

# colors
NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

echo -e ""
echo -e "⚙️  DEV Environment Setup"
echo -e ""
echo -e "➡️  This build takes ~ 30 seconds on a 150Mbps connection"
echo -e "➡️  and stores ~ ZGB of data on your disk."
echo -e ""

# deploying locally
echo -e ""
echo -e "⚙️  Starting environment with docker-compose..."
docker compose up -d
if [ "$?" -ne 0 ]; then
    echo -e ""
    echo -e "${RED}Error deploying the environment. Run $0 again.${NC} ❌"
    exit 1
else
    echo -e "${GREEN}Done!${NC} ✅"
fi

echo -e ""
echo -e "💻 Your DEV Environment is finished! ✅"
echo -e ""
echo -e "Here is some information about your environment:"
echo -e "PostgreSQL databases and credentials:"
echo -e "    👤 username: postgres"
echo -e "    🔑 password: wallaceEhLindo"
echo -e "    🗄️  database: postgres"
echo -e ""
echo -e "    👤 username: datalakeuser"
echo -e "    🔑 password: jpitawawa"
echo -e "    🗄️  database: datalake"
echo -e ""
