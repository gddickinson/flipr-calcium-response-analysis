# FLIPR Analysis Tool - Quick Start Guide

## Quick Installation

### 1. Install Anaconda
```bash
# Download from: https://www.anaconda.com/products/distribution
# Install with default settings
```

### 2. Create Environment
```bash
# Create and activate environment
conda create -n flipr python=3.9
conda activate flipr

# Install required packages
conda install pyqt pandas numpy openpyxl
conda install -c conda-forge pyqtgraph
```

### 3. Install FLIPR Analysis Tool
```bash
# Create directory
mkdir FLIPR_Analysis
cd FLIPR_Analysis

# Save flipr_analysis.py to this directory
```

### 4. Run Software
```bash
conda activate flipr
python flipr_analysis.py
```

## Basic Usage

### Data Loading
1. Click "Load Data" → Select .seq1 or .txt file
2. Configure analysis parameters: Analysis → Parameters

### Plate Configuration
- Select wells: Click individual wells or use row/column headers
- Label wells: Enter reagent info → Apply Label
- Log series: Enter starting concentration → Select wells in order

### Analysis
- Toggle artifact removal if needed
- Enable ionomycin normalization if required
- View traces: Raw/ΔF/F₀/Summary plots
- Export results to Excel

## Essential Parameters
- Artifact Start: 18 (default)
- Artifact End: 30 (default)
- Baseline Frames: 15 (default)
- Peak Start Frame: 20 (default)

## Quick Troubleshooting
```bash
# Environment issues
conda list  # Verify packages
conda install --force-reinstall package_name  # Reinstall if needed

# Path issues
echo $PATH  # Check conda in path
conda init  # Reinitialize if needed

# Package conflicts
conda install -c conda-forge package_name  # Alternative channel
```

## Key Files
- Input: .seq1 or .txt (FLIPR format)
- Output: .xlsx (analysis results)
- Layout: .json (plate configuration)

For detailed instructions, refer to the full user manual.
