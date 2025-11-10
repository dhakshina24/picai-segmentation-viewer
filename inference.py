"""Inference script for using the PiCAI nnUNet Docker container."""

import subprocess
import os
import shutil
import time
from config import INPUT_DIR, OUTPUT_DIR

def run_inference(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR, docker_image_name="picai_baseline_nnunet_processor:latest"):
  """Run the PiCAI Docker container for inference. """
  start = time.time()

  # Check if docker available
  if not shutil.which("docker"):
    raise EnvironmentError("Docker not found. Please ensure Docker is installed and running.")
  
  cmd = [
      "docker", "run", "--cpus=4", "--memory=32gb", "--shm-size=32gb", "--rm", 
      "-v", f"{input_dir}:/input",
      "-v", f"{output_dir}:/output",
      docker_image_name
  ]

  process = subprocess.Popen(
    cmd, 
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT, 
    text=True
  )

  # Stream Docker logs
  logs = ""
  for line in iter(process.stdout.readline, ""):
    logs += line
    yield logs, False
  process.wait()

  duration = round((time.time() - start) / 60, 2)

  if process.returncode != 0: 
    yield f"\nInference failed (exit code {process.returncode}).\n", False
  else:
    yield f"\nInference finished in {duration} minutes.\n", True