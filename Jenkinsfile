pipeline {
    agent any
    
    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '867344477317.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPO = 'ajio-recommender'
        ECS_CLUSTER = 'ajio-cluster'
        ECS_SERVICE = 'ajio-service'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Code checked out successfully'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('models/recommendation_model') {
                    sh 'docker build -t ${ECR_REPO}:latest .'
                    echo 'Docker image built successfully'
                }
            }
        }
        
        stage('Push to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    sh '''
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        docker tag ${ECR_REPO}:latest ${ECR_REGISTRY}/${ECR_REPO}:latest
                        docker push ${ECR_REGISTRY}/${ECR_REPO}:latest
                        echo "Image pushed to ECR successfully"
                    '''
                }
            }
        }
        
        stage('Deploy to ECS') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    sh '''
                        aws ecs update-service \
                            --cluster ${ECS_CLUSTER} \
                            --service ${ECS_SERVICE} \
                            --force-new-deployment \
                            --network-configuration "awsvpcConfiguration={subnets=[subnet-06a8818752ff88581],securityGroups=[sg-04cbdea49c5bd1865],assignPublicIp=ENABLED}" \
                            --region ${AWS_REGION}
                        echo "Deployed to ECS successfully"
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    sh '''
                        sleep 30
                        aws ecs describe-services \
                            --cluster ${ECS_CLUSTER} \
                            --services ${ECS_SERVICE} \
                            --region ${AWS_REGION} \
                            --query "services[0].runningCount" \
                            --output text
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed! App deployed to AWS successfully.'
        }
        failure {
            echo 'Pipeline failed! Check the logs.'
        }
    }
}
