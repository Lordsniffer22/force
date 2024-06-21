#!/bin/bash
# This is a docker installer for Ubuntu
# Scripted by OWORI NICHOLOUS [Blake]

print_pink() {
    echo -e "\e[1;95m$1\e[0m"
}

# Update and upgrade the system
sudo apt update -y
sudo apt upgrade -y

# Install necessary packages
sudo apt-get install -y curl apt-transport-https ca-certificates software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Set up the Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update the package index
sudo apt update -y

# Check if docker-ce is available in the repository
if apt-cache policy docker-ce | grep -q "Installed: (none)"; then
    # Install Docker
    sudo apt install -y docker-ce
    print_pink 'DOCKER HAS BEEN INSTALLED SUCCESSFULLY'
    sleep 3
    clear
else
    print_pink 'DOCKER IS ALREADY INSTALLED'
    sleep 3
    clear
fi

# Download the application files
wget -O fas.py https://raw.githubusercontent.com/Lordsniffer22/force/main/fas.py &>/dev/null
wget -O requirements.txt https://raw.githubusercontent.com/Lordsniffer22/rimoq/main/requirements.txt &>/dev/null
wget -O keybds.py https://raw.githubusercontent.com/Lordsniffer22/force/main/keybds.py &>/dev/null

#BUILD AN ENV
cat <<EOF > .env
RAVE_SECRET_KEY= FLWSECK-c0554fe039b959856c60903e8d14aedb-18fe9ef3dacvt-X
BOT_KEYS= 7059651547:AAEuJcszTHsGhd5-zHFQEU-INI79UVkO6zQ
ADMIN_CHAT_ID= 6448112643
EOF

# Create a Dockerfile
cat <<EOF > Dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD ["python3", "fas.py"]
EOF

# Build the Docker image
docker build -t force .

# Run the Docker container from the image
docker run -d --name joins --restart unless-stopped force

# Clean up the files
rm -rf Dockerfile fas.py requirements.txt keybds.py
