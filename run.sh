#!/bin/bash


sudo git pull

sudo docker build -t app-image ./app
sudo docker build -t nginx-image ./nginx

sudo docker run --name app-container -d -p 8000:8000 -p 27017:27017 -p 27016:27016 -p 27015:27015 app-image
sudo docker run --name nginx-container -d -p 80:80 -p 443:443 nginx-image
