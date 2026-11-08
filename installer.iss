; SARA AI 3.0 Enterprise Pro — Master Inno Setup Compiler Script
; Author: Muhammad Mubashar (Pasha Dev / @pasha804)
; Contact: mubasharmuhammad790@gmail.com | +923332656733

#define MyAppName "SARA AI 3.0 Enterprise Pro"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "Muhammad Mubashar (pasha804)"
#define MyAppURL "https://github.com/pasha804/SARA-AI-2.5-Pro"
#define MyAppExeName "SARA.exe"

[Setup]
AppId={{E6F7A8B9-C0D1-4E2F-A3B4-C5D6E7F80401}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\Programs\SARA AI 3.0 Pro
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=D:\MARAA AI
OutputBaseFilename=SARA-AI-3.0-Enterprise-Setup
SetupIconFile=D:\MARAA AI\SARA\resources\app\build\icon.ico
Compression=lzma2/fast
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "D:\MARAA AI\SARA\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\resources\app\build\icon.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\resources\app\build\icon.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Clean up legacy installations if found
procedure CurStepChanged(CurStep: TSetupStep);
var
  LegacyDir: string;
begin
  if CurStep = ssInstall then
  begin
    LegacyDir := ExpandConstant('{localappdata}\Programs\MYRAA');
    if DirExists(LegacyDir) then
    begin
      DelTree(LegacyDir, True, True, True);
    end;
  end;
end;

