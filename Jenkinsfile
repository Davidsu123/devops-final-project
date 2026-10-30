// CI pipeline of the final project.
// One Jenkinsfile for every branch (Multibranch Pipeline):
//   every branch (PIPE-01): 1. Docker build  2. Unit tests  3. Helm lint and template
//   main only    (PIPE-02): 4. Helm package  5. Docker push  6. Helm push
//   on failure: a message to Discord and an email
//
// Every build runs in a temporary pod with these containers:
//   python - runs the unit tests
//   helm   - the helm command line
//   docker - the docker command line
//   dind   - "Docker in Docker": a Docker engine that lives only inside this pod,
//            so the build does not use the Docker of the server

pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: python
      image: python:3.13-slim
      command: ["sleep"]
      args: ["infinity"]
    - name: helm
      image: alpine/helm:3.22.0
      command: ["sleep"]
      args: ["infinity"]
    - name: docker
      image: docker:29-cli
      command: ["sleep"]
      args: ["infinity"]
      env:
        - name: DOCKER_HOST
          value: unix:///var/run/docker.sock
      volumeMounts:
        - name: docker-socket
          mountPath: /var/run
    - name: dind
      image: docker:29-dind
      securityContext:
        privileged: true
      volumeMounts:
        - name: docker-socket
          mountPath: /var/run
        - name: docker-storage
          mountPath: /var/lib/docker
  volumes:
    - name: docker-socket
      emptyDir: {}
    - name: docker-storage
      emptyDir: {}
'''
    }
  }

  options {
    // Keep only the last 10 builds of every branch
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  environment {
    IMAGE = 'david147852/final-project-app'
    TAG = "b-${env.BUILD_NUMBER}"               // image tag, for example b-12
    CHART_VERSION = "1.0.${env.BUILD_NUMBER}"   // chart version, for example 1.0.12
    HELM_REPO = 'oci://registry-1.docker.io/david147852'
    NOTIFY_EMAIL = 'sulkis.d11@gmail.com'
  }

  stages {
    stage('1. Docker build') {
      steps {
        container('docker') {
          // Wait until the Docker engine in the dind container is ready
          timeout(time: 2, unit: 'MINUTES') {
            sh 'until docker info > /dev/null 2>&1; do sleep 2; done'
          }
          sh 'docker build -t $IMAGE:$TAG .'
        }
      }
    }

    stage('2. Unit tests') {
      steps {
        container('python') {
          sh 'pip install --no-cache-dir -r requirements-dev.txt'
          sh 'pytest -v'
        }
      }
    }

    stage('3. Helm lint and template') {
      steps {
        container('helm') {
          sh 'helm lint chart'
          sh 'helm template test chart'
        }
      }
    }

    stage('4. Helm package') {
      when { branch 'main' }
      steps {
        container('helm') {
          sh 'helm package chart --version $CHART_VERSION --app-version $TAG'
        }
      }
    }

    stage('5. Docker push') {
      when { branch 'main' }
      steps {
        container('docker') {
          withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials',
                                            usernameVariable: 'DOCKER_USER',
                                            passwordVariable: 'DOCKER_PASS')]) {
            sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
            sh 'docker push $IMAGE:$TAG'
          }
        }
      }
    }

    stage('6. Helm push') {
      when { branch 'main' }
      steps {
        container('helm') {
          withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials',
                                            usernameVariable: 'DOCKER_USER',
                                            passwordVariable: 'DOCKER_PASS')]) {
            sh 'echo $DOCKER_PASS | helm registry login registry-1.docker.io -u $DOCKER_USER --password-stdin'
            sh 'helm push final-project-chart-$CHART_VERSION.tgz $HELM_REPO'
          }
        }
      }
    }
  }

  post {
    failure {
      script {
        // Each message is sent on its own, so if one of them fails the other is still sent
        try {
          withCredentials([string(credentialsId: 'discord-webhook', variable: 'DISCORD_URL')]) {
            sh '''
              curl -fsS -X POST -H "Content-Type: application/json" \
                -d "{\\"content\\": \\"Build failed: $JOB_NAME #$BUILD_NUMBER $BUILD_URL\\"}" \
                "$DISCORD_URL"
            '''
          }
        } catch (err) {
          echo "Discord message was not sent: ${err}"
        }
        try {
          mail to: env.NOTIFY_EMAIL,
               subject: "Build failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
               body: "The build failed.\nDetails: ${env.BUILD_URL}"
        } catch (err) {
          echo "Email was not sent: ${err}"
        }
      }
    }
    fixed {
      script {
        try {
          mail to: env.NOTIFY_EMAIL,
               subject: "Build fixed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
               body: "The build is back to normal.\nDetails: ${env.BUILD_URL}"
        } catch (err) {
          echo "Email was not sent: ${err}"
        }
      }
    }
  }
}
