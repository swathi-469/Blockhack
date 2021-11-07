docker-dev-build:
	sudo docker build -t flask-docker-dev -f dev.Dockerfile .

docker-dev-run:
	docker run -it -v `pwd`:/usr/backend -w /usr/backend -p 5000:5000 flask-docker-dev
