$TaskAction = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "C:\path\to\logCleanup.ps1"
$TaskTrigger = New-ScheduledTaskTrigger -Daily -At 2:00am  

Register-ScheduledTask -Action $TaskAction -Trigger $TaskTrigger -TaskName "LogCleanupTask" -Description "Log Cleanup Task"
