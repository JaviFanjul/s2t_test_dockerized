
build:
	docker build -t audio-simulator .

run:
	docker run -it \
    	--rm \
  		--name audio_simulator \
  		-v /run/user/1000/pulse/native:/tmp/pulse_socket \
  		-e PULSE_SERVER=unix:/tmp/pulse_socket \
  		-u $(id -u):$(id -g) \
  		--device /dev/snd \
  		audio-simulator \
		bash
