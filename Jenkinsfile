pipeline {
    agent any

    environment {
        IMAGE_NAME = "lasyabagadi/lab4-app:latest"
        CONTAINER_NAME = "lab7_test_container"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh 'docker pull $IMAGE_NAME'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME'
            }
        }

        stage('Wait for API Readiness') {
            steps {
                script {
                    timeout(time: 60, unit: 'SECONDS') {
                        waitUntil {
                            def status = sh(
                                script: "curl -s http://localhost:8000/health",
                                returnStatus: true
                            )
                            return (status == 0)
                        }
                    }
                }
            }
        }

        stage('Test Valid Request') {
            steps {
                script {
                    def response = sh(
                        script: "curl -s -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d @valid.json",
                        returnStdout: true
                    ).trim()

                    echo "Valid Response: ${response}"

                    if (!response.contains("wine_quality")) {
                        error("Valid request failed — wine_quality missing")
                    }
                }
            }
        }

        stage('Test Invalid Request') {
            steps {
                script {
                    def response = sh(
                        script: "curl -s -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d @invalid.json",
                        returnStdout: true
                    ).trim()

                    echo "Invalid Response: ${response}"

                    if (!response.contains("error")) {
                        error("Invalid request did not return error")
                    }
                }
            }
        }

        stage('Stop Container') {
            steps {
                sh 'docker stop $CONTAINER_NAME || true'
                sh 'docker rm $CONTAINER_NAME || true'
            }
        }
    }

    post {
        success {
            echo "PIPELINE PASSED"
        }
        failure {
            echo "PIPELINE FAILED"
        }
    }
}
