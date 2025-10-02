terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

# Shared volume
resource "docker_volume" "shared" {
  name = "shared_data"
}

# Use pre-built images
resource "docker_image" "data_engineering" {
  name         = "data-engineering:latest"
  keep_locally = true
}

resource "docker_image" "data_science" {
  name         = "data-science:latest"
  keep_locally = true
}

resource "docker_image" "model_evaluation" {
  name         = "model-evaluation:latest"
  keep_locally = true
}

# Containers
resource "docker_container" "data_engineering" {
  name    = "data-engineering"
  image   = docker_image.data_engineering.image_id
  command = ["python", "pipeline_preprocessing.py"]
  volumes {
    volume_name    = docker_volume.shared.name
    container_path = "/shared"
  }
}

resource "docker_container" "data_science" {
  name    = "data-science"
  image   = docker_image.data_science.image_id
  command = ["python", "pipeline_training.py"]
  volumes {
    volume_name    = docker_volume.shared.name
    container_path = "/shared"
  }
  depends_on = [docker_container.data_engineering]
}

resource "docker_container" "model_evaluation" {
  name    = "model-evaluation"
  image   = docker_image.model_evaluation.image_id
  command = ["python", "evaluate_model.py"]
  volumes {
    volume_name    = docker_volume.shared.name
    container_path = "/shared"
  }
  depends_on = [docker_container.data_science]
}
