[Setup]
; Basic Application Information
AppName=Hoodie Weather Widget
AppVersion=0.0.5
AppPublisher=Hoodie Weather Team
AppPublisherURL=https://github.com/JayNightmare/hoodie-weather-widget
AppSupportURL=https://github.com/JayNightmare/hoodie-weather-widget/issues
AppUpdatesURL=https://github.com/JayNightmare/hoodie-weather-widget/releases
DefaultDirName={src}
DefaultGroupName=Hoodie Weather Widget
AllowNoIcons=yes
LicenseFile=..\LICENSE
InfoBeforeFile=..\docs\INSTALLATION_INFO.txt
InfoAfterFile=..\docs\POST_INSTALL_INFO.txt
OutputDir=..\output\installer_output
OutputBaseFilename=HoodieWeatherSetup
SetupIconFile=..\assets\icon.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=no
DisableReadyPage=no
ShowLanguageDialog=auto
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Visual Customization
WizardImageFile=..\assets\installer_image.bmp
WizardSmallImageFile=..\assets\installer_small.bmp
WizardImageStretch=no
WizardImageBackColor=$FFFFFF

; User Experience
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
CreateAppDir=yes
UsePreviousAppDir=yes
UsePreviousGroup=yes
UsePreviousSetupType=yes
UsePreviousTasks=yes

; Uninstaller
UninstallDisplayIcon={app}\HoodieWeather.exe
UninstallDisplayName=Hoodie Weather Widget
CreateUninstallRegKey=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startmenu"; Description: "Create Start Menu entry"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "startup"; Description: "Start with Windows (recommended)"; GroupDescription: "Startup Options"; Flags: checkedonce
Name: "context"; Description: "Add 'Check Weather' to right-click menu"; GroupDescription: "Integration"; Flags: unchecked; Check: IsAdminInstallMode

[Files]
; Main Application
Source: "..\output\dist\HoodieWeather.exe"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('..\output\dist\HoodieWeather.exe')
Source: "..\assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('..\assets\icon.ico')
Source: "..\src\config\widget_settings.json"; DestDir: "{app}\config"; Flags: ignoreversion onlyifdoesntexist; Check: FileExists('..\src\config\widget_settings.json')

; Documentation
Source: "..\README.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\USER_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion; Check: FileExists('USER_GUIDE.md')
Source: "..\CHANGELOG.md"; DestDir: "{app}\docs"; Flags: ignoreversion; Check: FileExists('CHANGELOG.md')

; Configuration and data directories
Source: "..\src\config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists('..\src\config')

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Hoodie Weather Widget"; Filename: "{app}\HoodieWeather.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Check: FileExists(ExpandConstant('{app}\icon.ico'))
Name: "{group}\Hoodie Weather Widget"; Filename: "{app}\HoodieWeather.exe"; WorkingDir: "{app}"; Check: not FileExists(ExpandConstant('{app}\icon.ico'))
Name: "{group}\User Guide"; Filename: "{app}\docs\USER_GUIDE.md"; Check: FileExists(ExpandConstant('{app}\docs\USER_GUIDE.md'))
Name: "{group}\{cm:UninstallProgram,Hoodie Weather Widget}"; Filename: "{uninstallexe}"

Name: "{autodesktop}\Hoodie Weather Widget"; Filename: "{app}\HoodieWeather.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon; Check: FileExists(ExpandConstant('{app}\icon.ico'))
Name: "{autodesktop}\Hoodie Weather Widget"; Filename: "{app}\HoodieWeather.exe"; WorkingDir: "{app}"; Tasks: desktopicon; Check: not FileExists(ExpandConstant('{app}\icon.ico'))

Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Hoodie Weather Widget"; Filename: "{app}\HoodieWeather.exe"; WorkingDir: "{app}"; Tasks: quicklaunchicon

[Registry]
; Auto-startup registry entry
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "HoodieWeatherWidget"; ValueData: "{app}\HoodieWeather.exe"; Flags: uninsdeletevalue; Tasks: startup

; Context menu integration
Root: HKCR; Subkey: "Directory\Background\shell\CheckWeather"; ValueType: string; ValueName: ""; ValueData: "Check Weather with Hoodie Widget"; Tasks: context
Root: HKCR; Subkey: "Directory\Background\shell\CheckWeather"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\HoodieWeather.exe,0"; Tasks: context
Root: HKCR; Subkey: "Directory\Background\shell\CheckWeather\command"; ValueType: string; ValueName: ""; ValueData: "{app}\HoodieWeather.exe"; Tasks: context; Flags: uninsdeletekey

; File associations (optional)
Root: HKCR; Subkey: ".weather"; ValueType: string; ValueName: ""; ValueData: "HoodieWeatherFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "HoodieWeatherFile"; ValueType: string; ValueName: ""; ValueData: "Hoodie Weather Data"; Flags: uninsdeletekey
Root: HKCR; Subkey: "HoodieWeatherFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\HoodieWeather.exe,0"
Root: HKCR; Subkey: "HoodieWeatherFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: "{app}\HoodieWeather.exe"

[Run]
; Option to launch after installation
Filename: "{app}\HoodieWeather.exe"; Description: "{cm:LaunchProgram,Hoodie Weather Widget}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any files created by the application
Type: files; Name: "{app}\config\user_settings.json"
Type: files; Name: "{app}\logs\*.log"
Type: dirifempty; Name: "{app}\config"
Type: dirifempty; Name: "{app}\logs"

[Code]
function IsAdmin(): Boolean;
begin
  Result := IsAdminInstallMode;
end;

function GetPythonPath(): String;
var
  PythonPath: String;
begin
  Result := '';
  
  // Check if Python is installed by looking in common locations
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.11\InstallPath', '', PythonPath) or
     RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.10\InstallPath', '', PythonPath) or
     RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.9\InstallPath', '', PythonPath) or
     RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.8\InstallPath', '', PythonPath) or
     RegQueryStringValue(HKEY_CURRENT_USER, 'SOFTWARE\Python\PythonCore\3.11\InstallPath', '', PythonPath) or
     RegQueryStringValue(HKEY_CURRENT_USER, 'SOFTWARE\Python\PythonCore\3.10\InstallPath', '', PythonPath) or
     RegQueryStringValue(HKEY_CURRENT_USER, 'SOFTWARE\Python\PythonCore\3.9\InstallPath', '', PythonPath) or
     RegQueryStringValue(HKEY_CURRENT_USER, 'SOFTWARE\Python\PythonCore\3.8\InstallPath', '', PythonPath) then
  begin
    Result := PythonPath;
  end;
end;

function InitializeSetup(): Boolean;
var
  PythonPath: String;
  ResultCode: Integer;
begin
  Result := True;
  
  // Check if this is a standalone executable installation
  if FileExists(ExpandConstant('{src}\dist\HoodieWeather.exe')) then
  begin
    // This is a standalone installation, no Python required
    Exit;
  end;
  
  // Check for Python installation
  PythonPath := GetPythonPath();
  if PythonPath = '' then
  begin
    if MsgBox('Python 3.8 or later is required to run Hoodie Weather Widget.' + #13#13 + 
              'Would you like to download and install Python now?' + #13#13 + 
              'Click "Yes" to visit python.org, or "No" to continue anyway.', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.python.org/downloads/', '', '', SW_SHOWNORMAL, ewNoWait, ResultCode);
    end;
  end
  else
  begin
    Log('Python found at: ' + PythonPath);
  end;
end;

procedure InitializeWizard();
begin
  // Custom welcome message
  WizardForm.WelcomeLabel2.Caption := 
    'This will install Hoodie Weather Widget on your computer.' + #13#13 +
    '🌤️ Get real-time weather updates' + #13 +
    '🧥 Smart hoodie recommendations' + #13 +
    '📍 Auto-location detection' + #13 +
    '🎨 Beautiful, modern design' + #13#13 +
    'Click Next to continue, or Cancel to exit.';
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  
  // Skip the Select Components page if we don't have components
  if PageID = wpSelectComponents then
    Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  SettingsFile: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Create default settings file if it doesn't exist
    SettingsFile := ExpandConstant('{app}\config\widget_settings.json');
    if not FileExists(SettingsFile) then
    begin
      // Create the config directory if it doesn't exist
      ForceDirectories(ExtractFileDir(SettingsFile));
      
      // Save basic default settings
      SaveStringToFile(SettingsFile, 
        '{' + #13#10 +
        '  "location": "auto",' + #13#10 +
        '  "units": "metric",' + #13#10 +
        '  "refresh_interval": 30,' + #13#10 +
        '  "show_notifications": true,' + #13#10 +
        '  "window_position": [100, 100],' + #13#10 +
        '  "theme": "auto"' + #13#10 +
        '}', False);
    end;
  end;
end;

function NeedRestart(): Boolean;
begin
  Result := False;
end;

// Custom messages for better user experience
procedure InitializeWizardStrings();
begin
  // Customize some standard messages
  WizardForm.ComponentsList.Items.Clear;
end;
