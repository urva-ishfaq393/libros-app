pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                echo '>>> Cloning repository from GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '>>> Building Docker image...'
                sh 'docker compose -f docker-compose.yml build'
            }
        }

        stage('Test') {
            steps {
                echo '>>> Running Selenium tests in Docker...'
                sh 'mkdir -p test-results'
                sh '''
                    docker compose -f docker-compose.pipeline.yml down --remove-orphans --volumes || true
                    docker compose -f docker-compose.pipeline.yml up \
                        --build \
                        --abort-on-container-exit \
                        --exit-code-from tests
                '''
            }
            post {
                always {
                    sh 'docker compose -f docker-compose.pipeline.yml down --remove-orphans --volumes || true'
                    junit allowEmptyResults: true, testResults: 'test-results/results.xml'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '>>> Deploying application...'
                sh 'docker compose -f docker-compose.yml down || true'
                sh 'docker compose -f docker-compose.yml up -d --build'
                echo '>>> App is live on port 5000'
            }
        }
    }

    post {
        always {
            script {
                // Try to get pusher email from GitHub webhook payload first
                // then fall back to git log
                def pusherEmail = ''

                try {
                    pusherEmail = env.GITHUB_PUSHER_EMAIL ?: ''
                } catch (e) {
                    pusherEmail = ''
                }

                if (!pusherEmail || !pusherEmail.contains('@')) {
                    pusherEmail = sh(
                        script: "git log -1 --pretty=format:'%ae'",
                        returnStdout: true
                    ).trim()
                }

                // If still not a valid email, use default
                if (!pusherEmail || !pusherEmail.contains('@')) {
                    pusherEmail = 'urvaishfaq1@gmail.com'
                }

                echo "Sending email to: ${pusherEmail}"

                def status   = currentBuild.currentResult ?: 'UNKNOWN'
                def jobName  = env.JOB_NAME
                def buildNum = env.BUILD_NUMBER
                def buildUrl = env.BUILD_URL
                def color    = (status == 'SUCCESS') ? 'green' : 'red'

                emailext(
                    to: "${pusherEmail}",
                    subject: "[Jenkins] ${status}: ${jobName} #${buildNum}",
                    body: """
<html><body>
<h2>Jenkins Pipeline Report</h2>
<table border="1" cellpadding="6">
  <tr><td><b>Job</b></td><td>${jobName}</td></tr>
  <tr><td><b>Build #</b></td><td>${buildNum}</td></tr>
  <tr><td><b>Status</b></td><td style="color:${color}"><b>${status}</b></td></tr>
  <tr><td><b>Pushed by</b></td><td>${pusherEmail}</td></tr>
  <tr><td><b>Build URL</b></td><td><a href="${buildUrl}">${buildUrl}</a></td></tr>
</table>
<p>See attached results.xml for Selenium test details.</p>
</body></html>
""",
                    mimeType: 'text/html',
                    attachmentsPattern: 'test-results/results.xml'
                )
            }
        }
    }
}
