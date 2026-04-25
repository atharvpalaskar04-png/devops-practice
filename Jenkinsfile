pipeline {
    agent any

    environment {
        IMAGE_NAME = "task-backend"
    }

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/atharvpalaskar04-png/devops-practice.git'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Load to kind') {
            steps {
                sh 'kind load docker-image $IMAGE_NAME --name devops-cluster'
            }
        }

        stage('Deploy to K8s') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }

        stage('Verify') {
            steps {
                sh 'kubectl get pods'
            }
        }
    }
}
