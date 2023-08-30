# CI/CD - Create a fully automated build pipeline to build and deploy code

Example scenario :

You can use default Apache installation and its index.html to demo the pipeline. Task is to modify the index.html publish to "dev" branch, which should trigger the build job which should put files into an artifact repository or s3 bucket. Once its success, trigger the deploy job to get the latest files into app server and restart Apache. And publish the status code of Apache web page as the outcome of the deploy job.

Optional: *Integrate with SonarQube to run a static code analysis to get the code coverage and pass the build based on that to trigger the deploy job*
