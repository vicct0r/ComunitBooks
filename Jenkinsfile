pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
        }
    }

    stages {
        stage('Python OK?') {
            steps {
                sh '''
                    python --version
                    pip --version
                '''
            }
        }
    }
}
