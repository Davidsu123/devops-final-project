pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:latest
    command: ['cat']
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  - name: python
    image: python:3.9-slim
    command: ['cat']
    tty: true
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKER_IMAGE_NAME     = "david147852/final-project-app"
        MONGO_PASSWORD = credentials('mongodb-password')
    }

    stages {
        stage('Checkout') {
            steps {
                container('docker') {
                    git branch: 'main', url: 'https://gitlab.com/sela-tracks/1116/students/david/final-project-app.git', credentialsId: 'gitlab-credentials'
                }
            }
        }

        stage('Unit Tests') {
            steps {
                container('python') {
                    sh 'pip install -r requirements.txt'
                    sh 'MONGO_PASSWORD=${MONGO_PASSWORD} pytest'
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                container('docker') {
                    script {
                        def imageTag = "b-${env.BUILD_NUMBER}"
                        docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS_ID) {
                            def customImage = docker.build(DOCKER_IMAGE_NAME + ":${imageTag}", '.')
                            customImage.push()
                            customImage.push('latest')
                        }
                    }
                }
            }
        }
    }
}
