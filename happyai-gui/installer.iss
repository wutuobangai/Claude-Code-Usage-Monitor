; Claude 额度小助手 · Windows 安装器（Inno Setup）· © Happy AI
; 一键安装：不需要管理员权限，装到当前用户目录，桌面自动出现图标，装完直接打开。
#define MyAppName "Claude 额度小助手"
#define MyAppExe "ClaudeQuotaHelper.exe"
#define MyAppVersion "1.0.0"
[Setup]
AppId={{7C1F3B2A-6E4D-4B8A-9C1D-HAPPYAI-CQH}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Happy AI · wutuobangai.top
AppPublisherURL=https://wutuobangai.top/
DefaultDirName={localappdata}\Programs\ClaudeQuotaHelper
DefaultGroupName={#MyAppName}
PrivilegesRequired=lowest
DisableWelcomePage=yes
DisableDirPage=yes
DisableProgramGroupPage=yes
DisableReadyPage=yes
OutputDir=Output
OutputBaseFilename=ClaudeQuotaHelper-Setup-{#MyAppVersion}
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExe}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
[Files]
Source: "dist\ClaudeQuotaHelper\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; DestName: "LICENSE-engine-MIT.txt"; Flags: ignoreversion
Source: "NOTICE-版权说明.md"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"
Name: "{autodesktop}\Happy AI 官网 · Claude 会员充值"; Filename: "https://wutuobangai.top/tool.html?id=claude-pro-sub&utm_source=claude-quota-app&utm_medium=installer&utm_content=desktop-shortcut"
[Run]
Filename: "{app}\{#MyAppExe}"; Description: "打开 {#MyAppName}"; Flags: nowait postinstall skipifsilent
