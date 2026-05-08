pipeline {
    agent any
    environment {
        COMPOSE_FILE = 'docker-compose.pipeline.yml'
        TEST_IMAGE = 'libros-tests:latest'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Code checked out from GitHub successfully."
            }
        }
        stage('Build Test Image') {
            steps {
                echo "Building test Docker image..."
                sh 'docker build -t libros-tests:latest ./libros-tests'
                echo "Test image built successfully."
            }
        }
        stage('Test') {
            steps {
                echo "Running Selenium tests..."
                sh '''
                    docker run --rm \
                        --network libros-app_libros-net \
                        libros-tests:latest
                '''
                echo "All tests passed!"
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
        always {
            script {
                def pusherEmail = sh(
                    script: "git log -1 --format='%ae'",
                    returnStdout: true
                ).trim()
                echo "Sending email to pusher: ${pusherEmail}"
                mail to: "${pusherEmail}",
                     subject: "Jenkins Pipeline - ${currentBuild.fullDisplayName} - ${currentBuild.currentResult}",
                     body: """
Build Result: ${currentBuild.currentResult}
Pipeline: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Build URL: ${env.BUILD_URL}

Test Stage: ${currentBuild.currentResult == 'SUCCESS' ? 'All 20 Selenium tests PASSED' : 'Tests FAILED - check logs'}
                     """
            }
        }
        success {
            echo "Pipeline completed successfully! App running on port 5001."
        }
        failure {
            echo "Pipeline failed. Check logs above."
            sh "docker compose -f ${COMPOSE_FILE} logs --tail=50 || true"
        }
    }
}
