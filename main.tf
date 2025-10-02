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
  name = "shared"
}

# Use images from Docker Hub
resource "docker_image" "data_engineering" {
  name         = "franzcastillo/data-engineering:latest"
  keep_locally = true
}

resource "docker_image" "data_science" {
  name         = "franzcastillo/data-science:latest"
  keep_locally = true
}

resource "docker_image" "model_evaluation" {
  name         = "franzcastillo/model-evaluation:latest"
  keep_locally = true
}

# Containers
resource "docker_container" "data_engineering" {
  name    = "data-engineering"
  image   = docker_image.data_engineering.image_id
  # Run preprocessing and write a ready flag in the shared volume
  command = ["sh", "-c", "python pipeline_preprocessing.py && touch /shared/01_preprocessing.done"]
  volumes {
    volume_name    = docker_volume.shared.name
    container_path = "/shared"
  }
}

resource "docker_container" "data_science" {
  name  = "data-science"
  image = docker_image.data_science.image_id
  # Wait for preprocessing to finish, then start training and write another flag
  command = ["sh", "-c", "while [ ! -f /shared/01_preprocessing.done ]; do sleep 1; done; python pipeline_training.py && touch /shared/02_training.done"]
  volumes {
    volume_name    = docker_volume.shared.name
    container_path = "/shared"
  }
  depends_on = [docker_container.data_engineering]
}

resource "docker_container" "model_evaluation" {
  name  = "model-evaluation"
  image = docker_image.model_evaluation.image_id
  # Wait for training to finish, then run evaluation
  command = ["sh", "-c", "while [ ! -f /shared/02_training.done ]; do sleep 1; done; python evaluate_model.py"]
  volumes {
    volume_name    = docker_volume.shared.name
    container_path = "/shared"
  }
  depends_on = [docker_container.data_science]
}
