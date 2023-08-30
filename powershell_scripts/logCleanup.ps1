# Set variables
$LogDirectory = "C:\Users\abhee\Desktop\LOGS"
$DaysToKeep = 7
$S3BucketName = "myfirstbucket19920394"
$OutputFile = "C:\Users\abhee\Desktop\LOGS\DeletedFilesAndStorage.txt"

# Create log directory and sample log files
if (-not (Test-Path -Path $LogDirectory)) {
    New-Item -Path $LogDirectory -ItemType Directory
}

# Remove old log files
$DeletedFiles = Get-ChildItem -Path $LogDirectory | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$DaysToKeep) }
$TotalDeletedSize = $DeletedFiles | Measure-Object -Property Length -Sum | Select-Object -ExpandProperty Sum

# Calculate freed storage percentage
$TotalDiskSize = (Get-WmiObject Win32_LogicalDisk | Where-Object { $_.DeviceID -eq "C:" }).Size
$FreedStoragePercent = ($TotalDeletedSize / $TotalDiskSize) * 100

# Output deleted files and freed storage percentage to a file
$DeletedFiles | ForEach-Object { $_.FullName } | Out-File -FilePath $OutputFile
"`nTotal Freed Storage Percentage: $FreedStoragePercent%" | Out-File -FilePath $OutputFile -Append

# Upload the output file to S3 bucket
$S3KeyName = "DeletedFilesAndStorage.txt"
Write-S3Object -BucketName $S3BucketName -File $OutputFile -Key $S3KeyName

# Clean up local output file
Remove-Item -Path $OutputFile
