import pulumi
import pulumi_docker as docker

from pulumi import Config

DOCKER_IO_USERNAME = Config("docker.io").require("username")
DOCKER_IO_PASSWORD = Config("docker.io").require("password")
DOCKER_IO_SERVER = Config("docker.io").get("server") or 'docker.io'

image = docker.Image("container-image",
    build=docker.DockerBuildArgs(
        platform="linux/amd64",
        context="container-image",
        dockerfile="container-image/Dockerfile",
    ),
    registry=docker.RegistryArgs(
        username=DOCKER_IO_USERNAME,
        password=DOCKER_IO_PASSWORD
    ),
    image_name="{0}/{1}/simple-website-with-variable:latest".format(DOCKER_IO_SERVER, DOCKER_IO_USERNAME),
    skip_push=True)
pulumi.export("imageName", image.image_name)
