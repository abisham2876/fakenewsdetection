pipeline {
    agent any
    environment {
        IMAGE_NAME = "verifai"
        CONTAINER  = "verifai_app"
        PORT       = "5000"
    }
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }
        stage('Validate Files') {
            steps {
                echo '🔍 Validating required project files...'
                script {
                    def required = ['app.py', 'train_model.py', 'requirements.txt', 'Dockerfile']
                    required.each { f ->
                        if (!fileExists(f)) error("Missing: ${f}")
                        echo "✅ ${f}"
                    }
                }
            }
        }
        stage('Lint Python') {
            steps {
                echo '🧹 Checking Python syntax...'
                // Windows-la sh command vela seiyaathu, so 'bat' use panrom
                bat "python -m py_compile app.py train_model.py"
            }
        }
        stage('Train Model') {
            steps {
                echo '🧠 Training ML model...'
                bat "pip install -r requirements.txt -q"
                bat "python train_model.py"
            }
        }
        stage('Docker Build') {
            steps {
                echo '🐳 Building Docker image...'
                bat "docker build -t %IMAGE_NAME%:latest ."
            }
        }
        stage('Deploy') {
            steps {
                echo '🚀 Deploying container...'
                bat "docker stop %CONTAINER% || ver > nul"
                bat "docker rm %CONTAINER% || ver > nul"
                bat "docker run -d --name %CONTAINER% -p %PORT%:5000 %IMAGE_NAME%:latest"
            }
        }
    }
}