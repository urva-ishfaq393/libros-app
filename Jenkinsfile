pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.pipeline.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Code checked out from GitHub successfully."
            }
        }

        stage('Build') {
            steps {
                echo "Building application inside Docker container..."
                sh 'docker pull python:3.11-slim'
                sh 'ls -la'
                echo "Build stage complete."
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying with docker compose..."
                sh "docker compose -f ${COMPOSE_FILE} down --remove-orphans || true"
                sh "docker compose -f ${COMPOSE_FILE} up -d"
                sh 'sleep 10'
                sh "docker compose -f ${COMPOSE_FILE} ps"
            }
        }

        stage('Verify') {
            steps {
                echo "Verifying deployment..."
                sh "docker compose -f ${COMPOSE_FILE} logs --tail=30 pipeline-web"
            }
        }
    }

    post {
        success {
            echo "Pipeline completed! App running on port 5001."
        }
        failure {
            echo "Pipeline failed. Check logs above."
            sh "docker compose -f ${COMPOSE_FILE} logs --tail=50 || true"
        }
    }
}
