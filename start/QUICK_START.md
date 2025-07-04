# 🚀 Quick Start: Building the Installer

## ❌ What NOT to do:
- Don't open `build.bat` in Inno Setup Compiler
- Don't try to compile batch files with Inno Setup

## ✅ Correct Steps:

### Method 1: Automated (Recommended)
1. **Open Command Prompt** in your project folder
2. **Run**: `build.bat`
3. **Choose**: Option 1 (Build Everything)
4. **Wait**: Script builds executable + installer automatically
5. **Done**: Find `HoodieWeatherSetup.exe` in `installer_output/` folder

### Method 2: Manual Steps
1. **Build Executable First**:
   ```cmd
   # In Command Prompt
   build.bat
   # Choose option 4 (Build Executable Only)
   ```

2. **Then Create Installer**:
   - Open **Inno Setup Compiler** (the application)
   - **File > Open**: Select `installer_script.iss`
   - **Build > Compile** (or press F9)
   - Find installer in `installer_output/` folder

## 🔍 Troubleshooting

### "File not found" errors in Inno Setup:
- Make sure you built the executable first (`dist/HoodieWeather.exe` must exist)
- Check that `docs/INSTALLATION_INFO.txt` exists
- Verify `LICENSE` file exists

### "Text is not inside a section" error:
- You're trying to compile the wrong file
- Open `installer_script.iss` (not `build.bat`)
- Batch files can't be compiled by Inno Setup

### Build script fails:
- Make sure Python is installed and in PATH
- Run `pip install -r requirements.txt`
- Check that all source files exist

## 📁 Expected File Structure After Build:
```
your-project/
├── dist/
│   └── HoodieWeather.exe          ← Executable (created first)
├── installer_output/
│   └── HoodieWeatherSetup.exe     ← Installer (created second)
├── HoodieWeatherWidget_Portable/  ← Portable version
├── installer_script.iss           ← Inno Setup script
└── build.bat                      ← Build automation script
```

## 🎯 Quick Summary:
1. **Command Prompt** → Run `build.bat` → Choose option 1
2. **Wait for completion**
3. **Find installer** in `installer_output/HoodieWeatherSetup.exe`
4. **Test installer** on a clean system
