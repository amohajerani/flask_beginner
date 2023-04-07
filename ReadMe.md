Launch application with NGINX and SSL on EC2:

https://dev.to/shadid12/how-to-deploy-your-node-js-app-on-aws-with-nginx-and-ssl-3p5l

Running flask with NGINX on docker:
https://www.youtube.com/watch?v=cjFjDXkfs6M&ab_channel=SriwWorldofCoding

On AWS:

- Create ububtu instance
- Add an inbound route to port 8000
- open the terminal
- sudo apt update
- sudo apt-get install docker.io
- sudo apt install docker-compose
- sudo docker-compose up -d
  or if you want load balancing:
- sudo docker-compose up -d --build --scale app=3
