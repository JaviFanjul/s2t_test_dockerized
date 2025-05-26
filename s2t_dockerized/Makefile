IMAGE_NAME = s2t-gpu-app
CONTAINER_NAME = s2t-gpu-container
DOCKERFILE = Dockerfile

VOLUME_TRANSCRIPTION = $(shell pwd)/transcription.txt

# Paths PulseAudio (PipeWire backend)
PULSE_SOCKET = /run/user/1000/pulse/native
PULSE_COOKIE = /run/user/1000/.config/pulse/cookie

prepare:
	mkdir -p config

build: prepare
	docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .

run:
	docker run --rm -it \
		--runtime=nvidia \
		-e NVIDIA_VISIBLE_DEVICES=0 \
		--name $(CONTAINER_NAME) \
		--device /dev/snd \
		--group-add audio \
		-v $(PULSE_SOCKET):/tmp/pulse_socket \
		-v $(PULSE_COOKIE):/tmp/pulse_cookie \
		-e PULSE_SERVER=unix:/tmp/pulse_socket \
		-e PULSE_COOKIE=/tmp/pulse_cookie \
		-v $(PWD)/chunks_sp1:/app/chunks_sp1 \
		-v $(PWD)/chunks_sp2:/app/chunks_sp2 \
		-v $(PWD)/transcription.txt:/app/transcription.txt \
		$(IMAGE_NAME) \
		bash

clean:
	docker rmi $(IMAGE_NAME)
