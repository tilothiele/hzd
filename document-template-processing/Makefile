
PHONY: build-image

build-image:
	docker build -t tilothiele/odt2pdf:latest .

bnp-image: build-image
	docker push tilothiele/odt2pdf:latest

odt2pdf:
	docker run --rm -e UNO_HOST=192.168.178.188 -e UNO_PORT=2002 tilothiele/odt2pdf:latest