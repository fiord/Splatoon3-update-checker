terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.51.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_compute_instance" "bot_instance" {
  name         = "splatoon3-update-checker-bot"
  machine_type = "e2-micro"
  
  # Spot VM to save costs (uncomment if desired, but might be unstable for a persistent bot)
  # scheduling {
  #   preemptible = true
  #   automatic_restart = false
  #   provisioning_model = "SPOT"
  # }
  
  # Standard cheap configuration
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 10 # 10GB is minimum standard
      type  = "pd-standard" # Standard disk is cheaper than SSD
    }
  }

  network_interface {
    network = "default"
    access_config {
      # Ephemeral public IP to allow internet access
    }
  }

  metadata = {
    # Using cloud-init to configure the instance
    user-data = templatefile("${path.module}/cloud-config.yaml.tftpl", {
      main_py_content = file("${path.module}/../main.py")
      discord_token   = var.discord_token
    })
  }

  service_account {
    # limit scopes to logging/monitoring for security
    scopes = ["logging-write", "monitoring-write"]
  }
}
