# Docker

Install Docker.

    sudo apt update
    sudo apt install apt-transport-https gnupg-agent
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=arm64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install docker-ce

Install docker-compose.

    sudo apt install build-essential python3 python3-pip
    sudo pip3 install docker-compose
