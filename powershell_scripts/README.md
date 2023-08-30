# Windows/PowerShell Task
Create a scheduled task using PowerShell to do the below task
- Create a log directory and put some sample log files into it.
- Write a logic to remove log files older than x days and output the list of deleted files into a file. Also get the total size of deleted files and show it as a percentage from the total Disk storage in the same file as freed storage percent.
- And publish this file into a s3 bucket
- Save this script as logCleanup.ps1
- And another script to provision the scheduled task using PowerShell

## Pre-requisites
Execute below commands in PowerShell terminal.
- Install AWS PowerShell module
  ```
  Install-Module -Name AWSPowerShell
  ```
- Change PowerShell execution policy
  ```
  Set-ExecutionPolicy -Scope LocalMachine Unrestricted
  ```
- Import AWS PowerShell module
  ```
  Import-Module AWSPowerShell
  ```
- Set AWS Access Key & Secret Access Key (Replace "IAM-USER-ACCESS-KEY" & "IAM-USER-SECRET-KEY")
  ```
  Set-AWSCredential -AccessKey IAM-USER-ACCESS-KEY -SecretKey IAM-USER-SECRET-KEY
  ```

  ## logCleanup.ps1 script output
  ![]()
