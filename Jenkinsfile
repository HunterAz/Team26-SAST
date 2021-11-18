pipeline {
        agent any
        stages {
		stage('Checkout') {
			steps {
			git branch:'main', url: 'https://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@github.com/HunterAz/Team26-SAST.git'
			}
		}
		stage('Code Quality Check via SonarQube') {
			steps {
				script {
					def scannerHome = tool 'SonarQube';
					withSonarQubeEnv('SonarQube') {
					sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=team26-sonar -Dsonar.sources=. -Dsonar.login=3b1424ffd23cfd68a7596f14dacffc65d2f2edbd"
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
