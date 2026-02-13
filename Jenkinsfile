pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "lasyabagadi/lab4-app"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . .venv/bin/activate
                python train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    env.CURRENT_ACCURACY = sh(
                        script: "jq .accuracy artifacts/metrics.json",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST')]) {
                        if (env.CURRENT_ACCURACY.toFloat() > BEST.toFloat()) {
                            env.IS_BETTER = "1"
                        } else {
                            env.IS_BETTER = "0"
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.IS_BETTER == "1" }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                usernameVariable: 'USER',
                                passwordVariable: 'PASS')]) {
                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker build -t $DOCKER_IMAGE:${BUILD_NUMBER} .
                    docker tag $DOCKER_IMAGE:${BUILD_NUMBER} $DOCKER_IMAGE:latest
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.IS_BETTER == "1" }
            }
            steps {
                sh '''
                docker push $DOCKER_IMAGE:${BUILD_NUMBER}
                docker push $DOCKER_IMAGE:latest
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**', fingerprint: true
        }
    }
}
