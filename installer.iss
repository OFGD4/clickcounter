#define AppName "ClickCount"
#define AppVersion "1.0.0"
#define AppExe "ClickCounter.exe"

[Setup]
AppId=OFGD4-ClickCount
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=OFGD4
DefaultDirName={localappdata}\Programs\{#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=dist
OutputBaseFilename=ClickCount-Setup
SetupIconFile=mkwa.ico
UninstallDisplayIcon={app}\{#AppExe}
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"

[Files]
Source: "dist\{#AppExe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "Start ClickCount"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\ClickCounter"