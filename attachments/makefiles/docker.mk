### DOCKER
# ¯¯¯¯¯¯¯¯¯¯¯


docker.push: ##
	docker tag yaml-merger:latest kfirfer/yaml-merger:${version}
	docker push kfirfer/yaml-merger:${version}
