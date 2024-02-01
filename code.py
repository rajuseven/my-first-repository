# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [START cloudbuild_python_yaml]
# [START cloudbuild_python_dependencies_yaml]
steps:
  # Install dependencies
  - name: python
    entrypoint: pip
    args: ["install", "-r", "requirements.txt", "--user"]
# [END cloudbuild_python_dependencies_yaml]

  # [START cloudbuild_python_tests_yaml]
  # Run unit tests
  - name: python
    entrypoint: python
    args: ["-m", "pytest", "--junitxml=${SHORT_SHA}_test_log.xml"] 
  # [END cloudbuild_python_tests_yaml]

  # [START cloudbuild_python_image_yaml]
  # Docker Build
  - name: 'gicr.io/cloud-builders/docker'
    args: ['build', '-t', 
           'us-central1-docker.pkg.dev/${PROJECT_ID}/${_ARTIFACT_REGISTRY_REPO}/myimage:${SHORT_SHA}', '.']
  # [END cloudbuild_python_image_yaml]

  # [START cloudbuild_python_push_yaml]
  # Docker push to Google Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push',  'us-central1-docker.pkg.dev/${PROJECT_ID}/${_ARTIFACT_REGISTRY_REPO}/myimage:${SHORT_SHA}']
  # [END cloudbuild_python_push_yaml]
  
  # [START cloudbuild_python_deploy_yaml]
  # Deploy to Cloud Run
  - name: google/cloud-sdk
    args: ['gcloud', 'run', 'deploy', 'helloworld-${SHORT_SHA}', 
           '--image=us-central1-docker.pkg.dev/${PROJECT_ID}/${_ARTIFACT_REGISTRY_REPO}/myimage:${SHORT_SHA}', 
           '--region', 'us-central1', '--platform', 'managed', 
           '--allow-unauthenticated']
  # [END cloudbuild_python_deploy_yaml]
  
# [START cloudbuild_python_logs_yaml]
# Save test logs to Google Cloud Storage
artifacts:
  objects:
    location: gs://${_BUCKET_NAME}/
    paths:
      - ${SHORT_SHA}_test_log.xml
# [END cloudbuild_python_logs_yaml]
# Store images in Google Artifact Registry 
images:
  - us-central1-docker.pkg.dev/${PROJECT_ID}/${_ARTIFACT_REGISTRY_REPO}/myimage:${SHORT_SHA}
# [END cloudbuild_python_yaml]