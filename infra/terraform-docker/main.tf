terraform {
  required_providers {
    docker = { source = "kreuzwerker/docker", version = "~> 3.0" }
  }
}

provider "docker" {
  # Windows + Docker Desktop: konek via named pipe
  host = "npipe:////./pipe/docker_engine"
  # Linux/macOS: host = "unix:///var/run/docker.sock"
}

resource "docker_network" "minimart" {
  name = "minimart-net"
}

resource "docker_image" "nginx" {
  name = "nginx:alpine"
}

resource "docker_container" "minimart" {
  name  = "minimart-terraform"
  image = docker_image.nginx.image_id

  networks_advanced {
    name = docker_network.minimart.name
  }

  ports {
    internal = 80
    external = 8080
  }
}

output "url" {
  value = "http://localhost:8080"
}
