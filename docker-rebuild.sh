docker stop cpl-manager
docker rm cpl-manager
docker build -t cpl-manager .
docker run -d -p 0.0.0.0:8080:80 --name cpl-manager cpl-manager
