#define AppName "ClickCount"
#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif
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
Filename: "{app}\{#AppExe}"; Description: "Start ClickCount"; Flags: nowait postinstall 

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\ClickCounter"