// =============================================================
// Jenkinsfile — Verifai CI/CD Pipeline
// Flow: GitHub push → Jenkins → Docker build → Deploy
// =============================================================

pipeline {

    agent any

    environment {
        IMAGE_NAME = "verifai"
        CONTAINER  = "verifai_app"
        PORT       = "5000"
    }

    triggers {
        githubPush()
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        // ── Stage 1: Checkout ──────────────────────────────────
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
                echo "Branch: ${env.GIT_BRANCH}"
                echo "Commit: ${env.GIT_COMMIT}"
            }
        }

        // ── Stage 2: Validate project files ───────────────────
        stage('Validate Files') {
            steps {
                echo '🔍 Validating required project files...'
                script {
                    def required = [
                        'app.py', 'train_model.py', 'requirements.txt',
                        'Dockerfile', 'templates/login.html',
                        'templates/register.html', 'templates/dashboard.html',
                        'static/auth.css', 'static/dashboard.css'
                    ]
                    required.each { f ->
                        if (!fileExists(f)) error("Missing: ${f}")
                        echo "✅ ${f}"
                    }
                }
            }
        }

        // ── Stage 3: Python lint check ─────────────────────────
        stage('Lint Python') {
            steps {
                echo '🧹 Checking Python syntax...'
                sh '''
                    python3 -m py_compile app.py
                    python3 -m py_compile train_model.py
                    echo "✅ Python syntax OK"
                '''
            }
        }

        // ── Stage 4: Train model ───────────────────────────────
        stage('Train Model') {
            steps {
                echo '🧠 Training ML model...'
                sh '''
                    pip install -r requirements.txt -q
                    python3 train_model.py
                    ls -lh model/
                    echo "✅ Model trained and saved"
                '''
            }
        }

        // ── Stage 5: Docker build ──────────────────────────────
        stage('Docker Build') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t $IMAGE_NAME:latest .
                    docker images | grep $IMAGE_NAME
                    echo "✅ Docker image built"
                '''
            }
        }

        // ── Stage 6: Deploy ────────────────────────────────────
        stage('Deploy') {
            steps {
                echo '🚀 Deploying container...'
                sh '''
                    # Stop existing container if running
                    docker stop $CONTAINER 2>/dev/null || true
                    docker rm   $CONTAINER 2>/dev/null || true

                    # Start new container
                    docker run -d \
                        --name $CONTAINER \
                        -p $PORT:5000 \
                        --restart unless-stopped \
                        $IMAGE_NAME:latest

                    echo "✅ Container started on port $PORT"
                    docker ps | grep $CONTAINER
                '''
            }
        }

        // ── Stage 7: Health check ──────────────────────────────
        stage('Health Check') {
            steps {
                echo '❤️ Checking app is live...'
                sh '''
                    sleep 5
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/login || echo "000")
                    echo "HTTP status: $STATUS"
                    if [ "$STATUS" != "200" ]; then
                        echo "❌ Health check failed (status: $STATUS)"
                        exit 1
                    fi
                    echo "✅ App is live at http://localhost:$PORT"
                '''
            }
        }

    }

    post {
        success {
            echo """
            ============================================
            ✅ PIPELINE SUCCESS
            ============================================
            Verifai is running at: http://localhost:${PORT}
            ============================================
            """
        }
        failure {
            echo """
            ============================================
            ❌ PIPELINE FAILED
            ============================================
            Check the stage logs above for details.
            ============================================
            """
        }
        always {
            echo "Build #${env.BUILD_NUMBER} finished — ${currentBuild.result ?: 'SUCCESS'}"
        }
    }
}
