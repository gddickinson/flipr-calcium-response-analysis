# FLIPR Analysis Tool - Complete Installation Guide Using Anaconda

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installing Anaconda](#installing-anaconda)
3. [Setting Up Your Environment](#setting-up-your-environment)
4. [Installing FLIPR Analysis Tool](#installing-flipr-analysis-tool)
5. [Running the Software](#running-the-software)
6. [Troubleshooting](#troubleshooting)

## System Requirements

Before starting, ensure your computer meets these minimum requirements:
- Windows 10, macOS 10.14+, or Linux
- 8GB RAM (16GB recommended)
- 10GB free disk space
- Internet connection for downloads
- Administrator privileges on your computer

## Installing Anaconda

### Step 1: Download Anaconda
1. Open your web browser
2. Go to: https://www.anaconda.com/products/distribution
3. Click the "Download" button for your operating system:
   - For Windows: "64-Bit Graphical Installer"
   - For Mac: Choose either "64-Bit Graphical Installer (Intel)" or "64-Bit Graphical Installer (M1)" depending on your processor
   - For Linux: "64-Bit (x86) Installer"

### Step 2: Install Anaconda (Windows)
1. Find the downloaded file (usually in Downloads folder)
2. Double-click "Anaconda3-xxxx.xx-Windows-x86_64.exe" (xxxx.xx will be the version number)
3. Follow the installation wizard:
   - Click "Next"
   - Click "I Agree" to accept the license
   - Choose "Just Me" (recommended)
   - Keep the default installation location (or note down if you change it)
   - IMPORTANT: Check both boxes for:
     - Add Anaconda3 to PATH
     - Register Anaconda3 as default Python
   - Click "Install"
   - Wait for installation (can take 15-30 minutes)
   - Click "Finish"
   - Optional: Click "Next" to learn about Anaconda Cloud
   - Click "Skip" for Visual Studio Code installation unless you want it

### Step 2 (Alternative): Install Anaconda (Mac)
1. Find the downloaded file in Downloads
2. Double-click "Anaconda3-xxxx.xx-MacOSX-x86_64.pkg"
3. Follow the installation wizard:
   - Click "Continue" through the introduction
   - Click "Continue" to read the license
   - Click "Agree" to accept the license
   - Click "Install" for standard installation
   - Enter your computer password if prompted
   - Wait for installation (can take 15-30 minutes)
   - Click "Close" when complete

### Step 3: Verify Installation
1. There are two ways to verify your installation:

   Method 1 - Using Anaconda Navigator:
   - Windows: Find "Anaconda Navigator" in Start Menu
   - Mac: Find "Anaconda Navigator" in Applications or Launchpad
   - Launch Anaconda Navigator
   - If it opens successfully, installation is complete

   Method 2 - Using Terminal/Command Prompt:
   - Windows: Open "Anaconda Prompt" from Start Menu
   - Mac: Open Terminal
   - Type:
     ```
     conda --version
     ```
   - You should see a version number (e.g., "conda 23.7.2")

## Setting Up Your Environment

### Method 1: Using Anaconda Navigator (Recommended for Beginners)
1. Open Anaconda Navigator
2. Click "Environments" in the left sidebar
3. Click "Create" at the bottom
4. In the dialog:
   - Name: enter "flipr"
   - Python version: select "3.9"
   - Click "Create"
5. Select your new "flipr" environment from the list
6. Switch to "All" in the package filter dropdown
7. Search for and install each package by checking the box and clicking "Apply":
   - pyqt
   - pandas
   - numpy
   - openpyxl
   - pyqtgraph

### Method 2: Using Anaconda Prompt/Terminal
1. Open Anaconda Prompt (Windows) or Terminal (Mac)
2. Create the environment:
   ```
   conda create -n flipr python=3.9
   ```
3. When prompted to proceed, type 'y' and press Enter
4. Activate the environment:
   ```
   conda activate flipr
   ```
5. Install required packages:
   ```
   conda install pyqt pandas numpy openpyxl
   conda install -c conda-forge pyqtgraph
   ```
6. Type 'y' when prompted for each installation

## Installing FLIPR Analysis Tool

### Step 1: Create a Working Directory
1. Open File Explorer (Windows) or Finder (Mac)
2. Navigate to your Documents folder
3. Create a new folder called "FLIPR_Analysis"

### Step 2: Save the Script
1. Open your preferred text editor:
   - Windows: Notepad or Anaconda's built-in Spyder IDE
   - Mac: TextEdit or Anaconda's built-in Spyder IDE
2. Copy the entire Python script provided
3. Save the file as "flipr_analysis.py" in your FLIPR_Analysis folder
4. If using TextEdit on Mac:
   - Click Format → Make Plain Text before saving
   - Ensure filename ends with .py not .txt

## Running the Software

### Method 1: Using Anaconda Prompt/Terminal (Recommended)
1. Open Anaconda Prompt (Windows) or Terminal (Mac)
2. Activate the environment:
   ```
   conda activate flipr
   ```
3. Navigate to your working directory:
   - Windows example:
     ```
     cd C:\Users\YourUsername\Documents\FLIPR_Analysis
     ```
   - Mac example:
     ```
     cd ~/Documents/FLIPR_Analysis
     ```
4. Run the script:
   ```
   python flipr_analysis.py
   ```

### Method 2: Using Spyder IDE
1. Open Anaconda Navigator
2. Select the "flipr" environment from the dropdown
3. Launch Spyder
4. Use File → Open to open flipr_analysis.py
5. Click the green "Run" triangle or press F5

## Troubleshooting

### Common Installation Issues

#### Anaconda Navigator Won't Open
1. Windows: Right-click and "Run as Administrator"
2. Mac: Check System Preferences → Security & Privacy for blocked apps

#### Package Installation Fails
1. Try updating conda:
   ```
   conda update conda
   ```
2. Try installing from different channels:
   ```
   conda install -c conda-forge package_name
   ```

#### Program Won't Start
1. Verify environment activation:
   ```
   conda activate flipr
   ```
2. Check package installation:
   ```
   conda list
   ```
3. Try reinstalling packages:
   ```
   conda install --force-reinstall package_name
   ```

### Environment Problems
If your environment becomes corrupted:
1. Create a new environment with a different name:
   ```
   conda create -n flipr_new python=3.9
   ```
2. Install packages in new environment
3. Delete old environment:
   ```
   conda env remove -n flipr
   ```

### Getting Help
If you encounter problems:
1. Check Anaconda documentation: https://docs.anaconda.com/
2. Verify all steps were followed exactly
3. Try uninstalling and reinstalling Anaconda completely
4. Contact your system administrator
5. [Insert your support contact information here]

## Maintenance and Updates

### Keeping Anaconda Updated
1. Open Anaconda Navigator
2. Click "Updates" in the left sidebar
3. Click "Update Index"
4. Update Anaconda and individual packages as needed

### Regular Maintenance
- Update Anaconda monthly
- Keep track of modifications to your environment
- Back up your analysis scripts regularly
- Check for FLIPR Analysis Tool updates

## Next Steps

After successful installation:
1. Read the FLIPR Analysis Tool User Manual
2. Try analyzing example data files
3. Familiarize yourself with the interface
4. Begin analyzing your own data

Remember:
- Always activate the flipr environment before running the program
- Save your work frequently
- Keep Anaconda and packages updated
- Report any issues to george.dickinson@gmail.com
