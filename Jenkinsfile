pipeline {
    agent any
    environment {
        IMAGE_NAME = "verifai"
        CONTAINER  = "verifai_app"
        PORT       = "5000"
        PYTHON_PATH = "C:\\Users\\abish\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }
        stage('Validate Files') {
            steps {
                echo 'Validating required project files...'
                script {
                    def required = ['app.py', 'train_model.py', 'requirements.txt', 'Dockerfile']
                    required.each { f ->
                        if (!fileExists(f)) error("Missing file: ${f}")
                        echo "Verified: ${f}"
                    }
                }
            }
        }
        stage('Lint Python') {
            steps {
                echo 'Checking Python syntax...'
                bat "chcp 65001 && \"%PYTHON_PATH%\" -m py_compile app.py train_model.py"
            }
        }
        stage('Train Model') {
            steps {
                echo 'Training ML model...'
                bat "chcp 65001 && set PYTHONUTF8=1 && \"%PYTHON_PATH%\" -m pip install flask flask-cors scikit-learn pandas numpy || exit 0"
                bat "chcp 65001 && set PYTHONUTF8=1 && \"%PYTHON_PATH%\" train_model.py"
            }
        }
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                bat "docker build -t %IMAGE_NAME%:latest ."
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                bat "docker stop %CONTAINER% || ver > nul"
                bat "docker rm %CONTAINER% || ver > nul"
                bat "docker run -d --name %CONTAINER% -p %PORT%:5000 %IMAGE_NAME%:latest"
            }
        }
    }
}