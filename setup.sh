#!/bin/bash

# Setup DEV Environment
# João Pedro Vasconcelos - jpvteixeira99@gmail.com
# First Version: 2022-11-30

# colors
NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

X_HASURA_ADMIN_SECRET="marceloVaiDar10"

echo -e ""
echo -e "⚙️  DEV Environment Setup"
echo -e ""
echo -e "➡️  This build takes ~ 30 seconds on a 150Mbps connection"
echo -e "➡️  and stores ~ 46.8MB of data on your disk."
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
echo -e "⚙️  Wait a few seconds while Hasura Endpoint is being deployed..."
count=1
while true; do
   curl http://localhost:8080
   if [ "$?" -ne 0 ]; then
      sleep 45
   else
      break
   fi
   if [ $count -eq 5 ]; then
      echo -e ""
      echo -e "${RED}Timeout. Run $0 again.${NC} ❌"
      exit 1
   fi
   count=$(($count+1))
done

# restoring hasura metadata
echo -e "⚙️  Restoring hasura metadata..."
RES=`curl -sSL -d @<(cat <<EOF
{
    "type": "replace_metadata",
    "args": $(cat hasura/hasura_metadata_2022_12_02_00_09_54_061.json)    
}
EOF
) -H "X-Hasura-Admin-Secret: $X_HASURA_ADMIN_SECRET" http://localhost:8080/v1/query`
echo -e $RES |grep "\{\"inconsistent_objects\":\[\],\"is_consistent\":true\}"
if [ "$?" -ne 0 ]; then
    echo -e ""
    echo -e "${RED}Error restoring Hasura metadata. Check your metadata file and/or the X_HASURA_ADMIN_SECRET value and run $0 again.${NC} ❌"
    exit 1
else
    echo -e "${GREEN}Done!${NC} ✅"
fi

echo -e ""
echo -e "💻 Your DEV Environment is finished! ✅"
echo -e ""
echo -e "Here is some information about your environment:"
echo -e "    🌐 hasura console: http://localhost:8080/console"
echo -e "    🌐 hasura endpoint: http://localhost:8080/v1/graphql"
echo -e "    🔑 x-hasura-admin-secret: $X_HASURA_ADMIN_SECRET"
echo -e ""
echo -e "PostgreSQL databases and credentials:"
echo -e "    👤 username: postgres"
echo -e "    🔑 password: wallaceEhLindo"
echo -e "    🗄️  database: postgres"
echo -e ""
echo -e "    👤 username: datalakeuser"
echo -e "    🔑 password: jpitawawa"
echo -e "    🗄️  database: datalake"
echo -e ""
