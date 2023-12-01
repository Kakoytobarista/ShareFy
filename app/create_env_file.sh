#!/bin/bash

echo '#NEW ENVS' > .env
echo 'SECRET_KEY=3b92e682738f236e079c2f0328472c2bbb7a09f4b593c950cb58a8e64626d0d2' >> .env
echo 'SECRET_KEY_REFRESH=3b92e682738f236e079c2f0328472c2bbb7a09f4b593c950cb58a8e64626d726' >> .env
echo 'ALGORITHM=HS256' >> .env
echo 'LIVE_TIME_TOKEN=60' >> .env

echo '' >> .env

echo '#MAIL ENVS' >> .env
echo 'MAIL_USERNAME=heydevworkaslan@outlook.com' >> .env
echo 'MAIL_PASSWORD=5899468kK25' >> .env
echo 'MAIL_FROM=heydevworkaslan@outlook.com' >> .env
echo 'MAIL_PORT=587' >> .env
echo 'MAIL_SERVER=smtp-mail.outlook.com' >> .env
echo 'MAIN_FROM_NAME=Web Mail by ShareFy' >> .env

echo '' >> .env

echo '#POSTGRES ENVS' >> .env
echo 'POSTGRES_DATABASE=mydatabase' >> .env
echo 'POSTGRES_USER=username' >> .env
echo 'POSTGRES_PASSWORD=password' >> .env

echo 'Environment file created successfully!'
