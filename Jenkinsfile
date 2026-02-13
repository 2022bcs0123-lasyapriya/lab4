pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "lasyabagadi/lab5-jenkins"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/2022bcs0123-lasyapriya/lab4.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Train and Evaluate Model') {
            steps {
                sh '''
                echo "Name: Bagadi Lasya Priya"
                echo "Roll No: 2022BCS0123"
                docker run $DOCKER_IMAGE python train.py
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    docker login -u $DOCKER_USER -p $DOCKER_PASS
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }
    }
}
