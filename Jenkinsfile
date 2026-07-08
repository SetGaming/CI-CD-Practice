pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    environment {
        AWS_REGION    = 'us-east-1'
        ECR_REGISTRY  = '992382545251.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY = '992382545251.dkr.ecr.us-east-1.amazonaws.com/avivhamoy/ci-cd-practice-app'
        LOCAL_IMAGE   = 'ci-cd-practice-app:local'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Image Metadata') {
            steps {
                script {
                    env.GIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()

                    env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_SHORT}"
                    env.IMAGE_URI = "${env.ECR_REPOSITORY}:${env.IMAGE_TAG}"
                }

                echo "Image tag: ${env.IMAGE_TAG}"
                echo "Image URI: ${env.IMAGE_URI}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    rm -rf .venv
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Validate Docker Compose') {
            steps {
                sh '''
                    docker compose config --quiet
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker compose build
                    docker image inspect "$LOCAL_IMAGE"
                '''
            }
        }

        stage('Login and Push to ECR') {
            steps {
                sh '''
                    set -eu

                    DOCKER_CONFIG_DIR="$(mktemp -d)"
                    export DOCKER_CONFIG="$DOCKER_CONFIG_DIR"

                    trap 'rm -rf "$DOCKER_CONFIG_DIR"' EXIT

                    aws ecr get-login-password \
                        --region "$AWS_REGION" |
                    docker login \
                        --username AWS \
                        --password-stdin "$ECR_REGISTRY"

                    docker tag "$LOCAL_IMAGE" "$IMAGE_URI"
                    docker push "$IMAGE_URI"
                '''
            }
        }
    }

    post {
        success {
            echo "CI pipeline completed successfully."
            echo "Published image: ${env.IMAGE_URI}"
        }

        failure {
            echo 'CI pipeline failed. Check the failed stage.'
        }

        always {
            echo "Build result: ${currentBuild.currentResult}"
        }
    }
}
