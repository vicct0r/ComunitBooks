pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/vicct0r/ComunitBooks.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    dockerImage = docker.build("community:${env.BUILD_NUMBER}")
                }
            }
        }
        
    }
}