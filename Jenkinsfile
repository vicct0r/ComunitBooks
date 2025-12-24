pipeline{
    agent any
    stages {
        stage('Test'){
            steps {
                // Roda a lógica do Django
                sh 'docker compose run --rm django_web python manage.py test'
            }
        }

        stage('Rebuild Aplication'){
            steps{
                sh 'cd /home/tornac/Desktop/ComunitBooks'
                sh 'docker compose down'
                sh 'docker compose up -d redis db'
                sh 'docker compose run --rm django_web python manage.py migrate'
                sh 'docker compose run --rm django_web python manage.py collectstatic --noinput'
                sh 'docker compose up --build -d'
            }
        }
    }
}