pipeline {
        agent any
        stages {
		stage('Checkout') {
			steps {
			git branch:'main', url: 'https://github.com/HunterAz/Team26-SAST.git'
			}
		}
		stage('Code Quality Check via SonarQube') {
			steps {
				script {
					def scannerHome = tool 'SonarQube';
					withSonarQubeEnv('SonarQube') {
					sh "${scannerHome}/bin/sonar-scanner 
					-Dsonar.projectKey=team26-sonar -
					Dsonar.sources=."
					}
				}
			}
		}    
        }
        post {
                always {
                recordIssues enabledForFailure: true, tool: sonarQube()
                }
        }
}
