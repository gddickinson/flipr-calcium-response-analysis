# FLIPR Analysis Tool - Complete Installation Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installing Miniconda](#installing-miniconda)
3. [Setting Up Your Environment](#setting-up-your-environment)
4. [Installing FLIPR Analysis Tool](#installing-flipr-analysis-tool)
5. [Running the Software](#running-the-software)
6. [Troubleshooting](#troubleshooting)

## System Requirements

Before starting, ensure your computer meets these minimum requirements:
- Windows 10, macOS 10.14+, or Linux
- 4GB RAM (8GB recommended)
- 5GB free disk space
- Internet connection for downloads

## Installing Miniconda

### Step 1: Download Miniconda
1. Open your web browser
2. Go to: https://docs.conda.io/en/latest/miniconda.html
3. Download the appropriate installer for your system:
   - For Windows: Click "Miniconda3 Windows 64-bit"
   - For Mac: Choose either "Miniconda3 macOS Intel x86 64-bit" or "Miniconda3 macOS Apple M1 64-bit" depending on your processor
   - For Linux: Click "Miniconda3 Linux 64-bit"

### Step 2: Install Miniconda (Windows)
1. Locate the downloaded file (usually in Downloads folder)
2. Double-click the installer
3. Click "Next"
4. Click "I Agree" to the license terms
5. Select "Just Me" when asked who to install for
6. Keep the default installation location (or note down if you change it)
7. IMPORTANT: Check both boxes for:
   - Add Miniconda3 to PATH
   - Register Miniconda3 as default Python
8. Click "Install"
9. Wait for installation to complete
10. Click "Finish"

### Step 2 (Alternative): Install Miniconda (Mac/Linux)
1. Open Terminal (Mac: use Spotlight search and type "Terminal")
2. Navigate to Downloads:
   ```
   cd ~/Downloads
   ```
3. Make the installer executable (replace filename with your downloaded version):
   ```
   chmod +x Miniconda3-latest-MacOSX-x86_64.sh
   ```
4. Run the installer:
   ```
   ./Miniconda3-latest-MacOSX-x86_64.sh
   ```
5. Press Enter to review the license
6. Type "yes" to accept
7. Press Enter to confirm location
8. Type "yes" when asked about initializing Miniconda3

### Step 3: Verify Installation
1. Close and reopen any terminal/command prompt windows
2. Test the installation:
   - Windows: Open "Anaconda Prompt" from Start Menu
   - Mac/Linux: Open Terminal
3. Type:
   ```
   conda --version
   ```
4. You should see a version number (e.g., "conda 4.10.3")

## Setting Up Your Environment

### Step 1: Create a New Environment
1. Open Anaconda Prompt (Windows) or Terminal (Mac/Linux)
2. Create a new environment called "flipr":
   ```
   conda create -n flipr python=3.9
   ```
3. When prompted to proceed, type 'y' and press Enter
4. Wait for the environment to be created

### Step 2: Activate the Environment
1. In the same window, type:
   ```
   conda activate flipr
   ```
2. Your prompt should change to show `(flipr)`

### Step 3: Install Required Packages
1. Install PyQt5:
   ```
   conda install pyqt
   ```
2. Install other required packages:
   ```
   conda install pandas numpy openpyxl
   ```
3. Install pyqtgraph:
   ```
   conda install -c conda-forge pyqtgraph
   ```
4. For each installation, type 'y' when prompted

## Installing FLIPR Analysis Tool

### Step 1: Create a Working Directory
1. Open File Explorer (Windows) or Finder (Mac)
2. Create a new folder called "FLIPR_Analysis" somewhere easy to find (e.g., Documents)

### Step 2: Save the Script
1. Open a text editor (e.g., Notepad on Windows, TextEdit on Mac)
2. Copy the entire Python script provided
3. Save the file as "flipr_analysis.py" in your FLIPR_Analysis folder
4. Make sure it saves with the .py extension (not .txt)

## Running the Software

### Step 1: Navigate to Working Directory
1. Open Anaconda Prompt (Windows) or Terminal (Mac/Linux)
2. Activate the environment:
   ```
   conda activate flipr
   ```
3. Navigate to your working directory:
   ```
   cd path/to/FLIPR_Analysis
   ```
   Replace "path/to" with the actual path to your folder
   
   Example (Windows):
   ```
   cd C:\Users\YourUsername\Documents\FLIPR_Analysis
   ```
   
   Example (Mac/Linux):
   ```
   cd ~/Documents/FLIPR_Analysis
   ```

### Step 2: Launch the Program
1. Run the script:
   ```
   python flipr_analysis.py
   ```
2. The FLIPR Analysis Tool window should appear

### Step 3: Test the Installation
1. The main window should show a 96-well plate layout
2. Try loading a sample data file
3. Check that plots can be displayed

## Troubleshooting

### Common Installation Issues

#### "conda not recognized" Error
- Windows: Reinstall Miniconda and ensure you check "Add to PATH"
- Mac/Linux: Add to PATH manually:
  ```
  export PATH=~/miniconda3/bin:$PATH
  ```

#### Package Installation Fails
1. Try updating conda:
   ```
   conda update conda
   ```
2. Try installing packages one at a time
3. If a package fails, try with pip:
   ```
   pip install package_name
   ```

#### Program Won't Start
1. Verify Python version:
   ```
   python --version
   ```
   Should show Python 3.9.x
2. Check all packages are installed:
   ```
   pip list
   ```
   Look for:
   - PyQt5
   - pandas
   - numpy
   - pyqtgraph
   - openpyxl

### Getting Help
If you encounter problems:
1. Make sure you followed all steps exactly
2. Try uninstalling and reinstalling everything
3. Contact your system administrator
4. [Insert your support contact information here]

## Next Steps

Once installation is complete:
1. Read the User Manual for operation instructions
2. Try loading example data files
3. Familiarize yourself with the interface
4. Start analyzing your own data

Remember to:
- Keep your conda environment active when using the program
- Update packages periodically
- Save your work frequently
