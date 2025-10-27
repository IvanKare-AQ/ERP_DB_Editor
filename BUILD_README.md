# ERP Database Editor - Build Instructions

This document explains how to build cross-platform executables for the ERP Database Editor.

## Automated Builds (GitHub Actions)

### Triggering Builds

Builds are automatically triggered when:
1. **Commit Message Trigger**: Include `#BUILD` in your commit message
2. **Manual Trigger**: Use the GitHub Actions workflow_dispatch feature

### Example Commits
```bash
git commit -m "Add new feature #BUILD"
git push origin main
```

### Build Platforms

The automated build creates executables for:
- **Windows x86** (64-bit)
- **Windows ARM** (ARM64)
- **Ubuntu** (Linux x86_64)
- **macOS** (Universal)

### Build Output

Each build creates:
- Directory distribution (not single file)
- Platform-specific executables
- GitHub Release with downloadable ZIP files

## Local Builds

### Prerequisites

1. **Python 3.11+** installed
2. **All dependencies** from `requirements.txt`
3. **PyInstaller** installed

### Quick Build

```bash
# Run the automated build script
python build_local.py
```

### Manual Build

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build using spec file
pyinstaller ERP_DB_Editor.spec

# Or build directly
pyinstaller --onedir --windowed --name "ERP_DB_Editor" src/main.py
```

### Build Output

- **Location**: `dist/ERP_DB_Editor/`
- **Executable**: Platform-specific executable in the dist folder
- **Dependencies**: All required libraries bundled

## Platform-Specific Notes

### Windows
- **Executable**: `ERP_DB_Editor.exe`
- **Dependencies**: All DLLs and libraries included
- **Requirements**: Windows 10/11

### macOS
- **Executable**: `ERP_DB_Editor.app`
- **Dependencies**: All frameworks included
- **Requirements**: macOS 10.15+

### Ubuntu/Linux
- **Executable**: `ERP_DB_Editor`
- **Dependencies**: System libraries included
- **Requirements**: Ubuntu 20.04+

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Build Failures**
   - Check Python version (3.11+ recommended)
   - Ensure all dependencies are installed
   - Clean previous builds: `rm -rf build dist`

3. **Large File Sizes**
   - This is normal for PyInstaller builds
   - Directory distribution includes all dependencies
   - Consider using `--exclude-module` for unused libraries

### Build Optimization

To reduce file size, you can exclude unused modules:

```python
# In ERP_DB_Editor.spec
excludes = [
    'matplotlib',
    'scipy',
    'jupyter',
    'pytest',
    # Add other unused modules
]
```

## GitHub Actions Workflow

### Workflow Features

- **Conditional Builds**: Only builds when `#BUILD` is in commit message
- **Multi-Platform**: Builds for all target platforms simultaneously
- **Artifact Upload**: Creates downloadable ZIP files
- **Automatic Releases**: Creates GitHub releases with all platforms

### Workflow File

The workflow is defined in `.github/workflows/build-executables.yml`

### Manual Trigger

You can manually trigger builds from the GitHub Actions tab:
1. Go to Actions tab in GitHub
2. Select "Build Cross-Platform Executables"
3. Click "Run workflow"
4. Choose branch and click "Run workflow"

## Code Signing (Future Enhancement)

For production distribution, consider adding code signing:

### Windows
- Use `signtool.exe` for Windows executables
- Requires code signing certificate

### macOS
- Use `codesign` for macOS applications
- Requires Apple Developer certificate

### Linux
- Use GPG signing for packages
- Not typically required for executables

## Support

For build issues:
1. Check the GitHub Actions logs
2. Review this documentation
3. Test local builds first
4. Create an issue if problems persist
