build:
	docker build -t cpl-manager .
run: build
	docker run -d -p 0.0.0.0:8080:80 --name cpl-manager cpl-manager
clean:
	docker stop cpl-manager
	docker rm cpl-manager
update: clean build run
