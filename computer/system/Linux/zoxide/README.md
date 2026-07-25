# zoxide



## linux



* install the tool
sudo apt install zoxide
* writing into the system files
echo 'eval "$(zoxide init bash)"' >> ~/.bashrc # profile 还是更适合环境变量。



## window



* winget install ajeetdsouza.zoxide



```{text}

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned



New-Item -ItemType File -Force $PROFILE.CurrentUserAllHosts



Add-Content $PROFILE.CurrentUserAllHosts "`nzoxide init powershell | Out-String | Invoke-Expression"



. $PROFILE.CurrentUserAllHosts



Get-Command z



```

