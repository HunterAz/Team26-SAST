pipeline {
        agent any
        stages {
		stage('Checkout SCM') {
			steps {
				checkout scm
				// Create a temporary docker with same volume (Path must exist in both jenkins docker and host)
				sh "docker run --name meok_data -v meok_volume:/var/lib/docker/volumes/meok_volume/_data bash"
				// Copy git files into the volume
				sh "docker cp . meok_data:var/lib/docker/volumes/meok_volume/_data/"
				// Remove temporary docker
				sh "docker rm -f meok_data"
			}
		}
                stage('OWASP DependencyCheck') {
                        steps {
                                dependencyCheck additionalArguments: '''
                                -o "./" 
                                -s "./"
                                -f "ALL"
				--enableExperimental
                                ''', odcInstallation: 'OWASP-Dependency-Check'
                        }
                }
                stage('Clean') {
                    steps {
			sh "docker rm -f meok_nginx"
                        sh "docker rm -f meok_flask"
                        sh "docker rm -f meok_mysql"
                    }
                }
                stage('Build') {
                    steps {
                            sh "docker image build /var/lib/docker/volumes/meok_volume/_data/nginx/ -t meok_nginx"
                            sh "docker image build /var/lib/docker/volumes/meok_volume/_data/flask/ -t meok_flask"
                            sh "docker image build /var/lib/docker/volumes/meok_volume/_data/mysql/ -t meok_mysql"
                    }
                }
                stage('Deploy') {
                    steps {
			//sh "bash /var/lib/docker/volumes/meok_volume/_data/build.sh"
                        sh '''
                        docker run -d  \
                            --name meok_nginx \
			    --user 1000:1000 \
                            --volume "/var/lib/docker/volumes/meok_volume/_data/nginx/logs/":"/var/log/nginx/" \
                            --publish 80:80 \
                            --publish 443:443 \
                            --network meok_frontend \
                            meok_nginx
                        '''
			sh '''
                        docker run -d  \
                            --name meok_mysql \
                            --volume "/var/lib/docker/volumes/meok_volume/_data/mysql/database_data":"/var/lib/mysql" \
                            --env-file "/var/lib/docker/volumes/meok_volume/_data/mysql/.env" \
                            --network meok_backend \
                            meok_mysql \
			    mysqld --default-authentication-plugin=mysql_native_password
                        '''
                        sh '''
                        docker run -d  \
                            --name meok_flask \
                            --volume "/var/lib/docker/volumes/meok_volume/_data/flask/website":"/home/meok/website" \
                            --env-file "/var/lib/docker/volumes/meok_volume/_data/flask/.env" \
                            --network meok_frontend \
                            meok_flask
                        '''
                        sh 'docker network connect meok_backend meok_flask'
		    } 
                }
                stage('Testing') {
			agent {
				docker {
					image 'python:3.8.12-buster'
					args '-u root'
				}
			}
			steps {
				sh 'apt-get update'
				sh 'apt-get install -y python3-dev default-libmysqlclient-dev build-essential'
                                sh 'pip install -r flask/requirements.txt --ignore-installed'
				sh 'python flask/test_login_unit_testing.py'
				sh 'python flask/test_forum.py'
                                sh 'pytest flask/test_validation_inputs.py'
                                sh 'pytest flask/test_login_integration_testing.py'
                                sh 'pytest flask/test_logout_integration_testing.py'
                    }
                }
        }
        post {
                success {
                        dependencyCheckPublisher pattern: 'dependency-check-report.xml'
                }
        }
}
