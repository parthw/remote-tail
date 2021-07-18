
pipeline {

  agent any

  stages {

    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM', branches: [[name: "main"]], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'my-jenkins-key', url: 'git@github.com:parthw/remote-tail.git']]])
        script {
            env.commit_id = "${sh(script:'git rev-parse --short HEAD', returnStdout: true).trim()}"
        }
      }
    }

    stage('Build') {
      steps {
        sh "DOCKER_BUILDKIT=1 docker build -f Dockerfile.build -t rtail-agent-build:latest --output type=local,dest=out ."
      }
    }
    
    stage('Lint Record') {
      steps {
        recordIssues(tools: [pyLint(pattern: '**/pylint.log')])
      }
    }

    stage('Image push') {
      steps {
        sh "docker build -t XXXXXX.dkr.ecr.ap-south-1.amazonaws.com/remote-tail-agent:${env.commit_id} ."
        sh "docker push XXXXXXX.dkr.ecr.ap-south-1.amazonaws.com/remote-tail-agent:${env.commit_id}"
      }
    }

    stage('Deployment') {
      steps {
        sh "sed 's/{{image_id}}/'${env.commit_id}'/g' kubernetes-deployment.yaml | kubectl apply -f -"
        sh "kubectl rollout status deployment/remote-tail-agent -n remote-tail"
      }
    }
  }

}