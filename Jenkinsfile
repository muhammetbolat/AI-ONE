#!/usr/bin/env groovy
@Library('PipelineExternalLib@master') _

// cmdb variables
appServiceName = "Onent_Planlama"
softwareModuleName = "ai-one"
appVersion = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"		// application version

// artifacatory variables
artifactoryHostAddress = "artifactory.turkcell.com.tr"
genericArtifactRepoAddress = "local-pypi-dist-dev"
applicationServiceName = "Onent_Planlama"
artifactName = "ai-one"
openshiftProjectName = "devops-gens"
gitCredentialSecret = "ocp-git-gens"
artifactoryDeployerCredentialID = "jenkins-gens-artifactory"

// docker/openshift variables
newImageUrl = ""															// newly created docker image address
openshiftProjectName = "sharedlocation"								     	// openshift namespace
openshiftClientToken = "ocpt1-credential-noderunner-stable"					// openshift credential name in Jenkins
deploymentConfigTemplate = "openshift/ocp-deploy.yaml"                     // openshift deployment pod config template yaml file
dockerRepo = "local-docker-dist-dev"										// docker registry repo name on artifacatory
dockerRegistryBaseUrl = "${artifactoryHostAddress}/${dockerRepo}/com/turkcell"	// docker registry address
// artifactory virtual pypi repo

artifactoryPypiUrl = "https://artifactory.turkcell.com.tr/artifactory/api/pypi/virtual-pypi/simple/"

pipeline 
{

    agent none

    options 
    {
        timestamps()
    }

	environment 
    {
        m2 = "/home/jenkins/.m2"
		mainBranch = "releasable"
	}

    stages 
    {

        stage('CI') 
        {

          	agent { label 'devops-gens-js-python' }

            stages  
            {
				
				stage('Build Package') 
                {
					steps
                    {
						script 
                        {
                            sh "mkdir dist"
						}
					}
				}
				
				stage('publish artifact') 
                {
					when
                    {
						branch "${mainBranch}"
					}
					steps
                    {
						script 
                        {
                            sh "python3.6 -m twine upload --repository artifactory-dev dist/ai-${appVersion}*"
							//sh "python3.6 -m twine upload --config-file .pypirc-dev --repository artifactory-dev dist/ai-${appVersion}*"
						}
					}
				}
              
                stage('deploy to TEST') 
                {
                    agent { label 'devops-gens-js-python' }
                    when 
                    {
                        branch "${mainBranch}"
                        beforeInput true
                    }
                    input 
                    {
                        message "Approve deploy to TEST?"
                        id "TestDeploy"
                        ok "YES"
                        submitter "tckakarca,tcmbolat,tcahakca,KOKPIT_ENT"
                    }
                    steps 
                    {
                        script 
                        { 
                        openshiftAppName = "${appServiceName}"
                        newImageUrl = "${dockerRegistryBaseUrl}/${openshiftAppName}/${softwareModuleName}:${appVersion}"
                            //deploy the new docker image to openshift TEST namespace
                            openshiftClient 
                            {
                                openshift.apply(openshift.process(readFile(file: deploymentConfigTemplate), "-p", "REGISTRY_URL=${newImageUrl}"))
                                def dc = openshift.selector('dc', "${softwareModuleName}")
                                dc.rollout().status()
                            }
                        }
                    } 
                    
                    post 
                    {
                        always 
                        {
                            echo "CI stage finished."
                        }
                        success 
                        {
                            echo "CI stage successfullly completed"
                            script
                            {
                                sh "echo status update running on jira"
                            }
                        }
                        failure 
                        {
                            echo "CI stage failed!"
                            script
                            {
                                sh "echo status update running on jira"
                            }
                        }
                    }
                }
            }
        }
    }
	post {
        always {
            echo "this step executing ALWAYS"
        }
        success {
            echo "this step executing SUCCESS"
        }
        failure {
            echo "this step executing FAILURE"
        }
        cleanup {
            echo "this step executing CLEANUP"
        }
    }
}

def openshiftClient(Closure body) 
{
    openshift.withCluster('insecure://kubernetes.default.svc') 
    {
        openshift.withCredentials(openshiftClientToken) 
        {
            openshift.withProject(openshiftProjectName) 
            {
                body()
            }
        }
    }
}
