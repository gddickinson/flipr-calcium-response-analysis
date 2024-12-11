# FLIPR Analysis Tool User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Main Interface](#main-interface)
5. [Data Loading and Processing](#data-loading-and-processing)
6. [Well Selection and Labeling](#well-selection-and-labeling)
7. [Analysis Features](#analysis-features)
8. [Visualization Options](#visualization-options)
9. [Data Export](#data-export)
10. [Tips and Troubleshooting](#tips-and-troubleshooting)

## Introduction
The FLIPR Analysis Tool is designed for analyzing calcium imaging data from FLIPR experiments. It provides an intuitive interface for data processing, visualization, and analysis of calcium responses in 96-well plate formats.

## Installation

### Setting up the Environment
1. Install Miniconda or Anaconda from https://docs.conda.io/en/latest/miniconda.html
2. Open a terminal (or Anaconda Prompt on Windows)
3. Create a new conda environment:
```bash
conda create -n flipr python=3.9
conda activate flipr
```

### Installing Required Packages
Install the required packages using conda and pip:
```bash
conda install pyqt numpy pandas
conda install -c conda-forge pyqtgraph openpyxl
```

### Running the Tool
1. Clone or download the source code
2. Navigate to the code directory:
```bash
cd path/to/flipr-analysis
```
3. Run the tool:
```bash
python flipr_analysis.py
```

## Getting Started

### System Requirements
- Python 3.9 or later
- Required libraries:
  - PyQt5: GUI framework
  - pyqtgraph: Scientific plotting
  - pandas: Data handling
  - numpy: Numerical operations
  - openpyxl: Excel export support
- Sufficient memory to handle FLIPR data files

### Data Format
The tool accepts FLIPR output files (.seq1) with the following characteristics:
- Tab-delimited text format
- Metadata in the first column
- Raw time series intensity values from column 5 onwards
- First row containing header values

## Main Interface

### Layout Components
1. **Plate Layout Tab**:
   - 96-well plate grid
   - Well labeling controls
   - Action buttons for layout management
2. **Analysis Tab**:
   - Plot controls
   - Analysis parameters
   - Results display
   - Export functionality

### Menu Bar
- **Analysis**: Access to analysis parameters
- **Help**: Access to this user manual and about information

## Data Loading and Processing

### Loading Data
1. Click "Load Data" to open a file selection dialog
2. Select your .seq1 file
3. The data will be loaded and the well plate grid will be enabled

### Analysis Parameters
Access via Analysis → Parameters to set:
- Artifact Start Frame: Start of injection artifact
- Artifact End Frame: End of injection artifact
- Baseline Frames: Number of frames for baseline calculation
- Peak Start Frame: Frame to start peak detection from

## Well Selection and Labeling

### Selection Methods
- **Individual Wells**: Click on wells to select/deselect
- **Row Selection**: Click row labels (A-H)
- **Column Selection**: Click column labels (1-12)
- **All Wells**: Click top-left corner

### Labeling Options
1. **Simple Label**:
   - Enter agonist name
   - Enter concentration (µM)
   - Enter sample ID
   - Select color (optional)
   - Click "Apply Label"

2. **Log10 Series**:
   - Enter starting concentration
   - Select multiple wells (in order)
   - System automatically calculates dilution series

## Analysis Features

### Injection Artifact Removal
- Toggle "Remove Injection Artifact" checkbox
- Removes specified frames around injection point
- Updates all plots automatically

### Ionomycin Normalization
- Toggle "Normalize to Ionomycin" checkbox
- Calculates responses as percentage of ionomycin response
- Groups by sample ID if multiple samples present
- Automatically excludes ionomycin groups from normalized plots

### Data Processing
The tool automatically:
1. Calculates ΔF/F₀ from raw intensity values
2. Removes injection artifacts if enabled
3. Calculates peak responses
4. Groups data based on labels

## Visualization Options

### Raw Traces
- Shows raw intensity values
- Individual well traces
- Color-coded by group
- Toggle with "Raw Traces" button

### ΔF/F₀ Traces
- Shows normalized calcium responses
- Individual well traces
- Color-coded by group
- Toggle with "ΔF/F₀ Traces" button

### Summary Plots
Four tabs available:
1. **Individual Traces**:
   - All ΔF/F₀ traces grouped by condition
   - Semi-transparent individual traces
   - Color-coded by group

2. **Mean Traces**:
   - Mean ΔF/F₀ response per group
   - SEM shown as shaded region
   - Clear legend for each group

3. **Peak Responses**:
   - Bar graph of peak responses
   - Error bars show SEM
   - Groups clearly labeled

4. **Normalized to Ionomycin** (when enabled):
   - Responses as percentage of ionomycin
   - Error bars show SEM
   - Automatically excludes ionomycin controls
   - Maintains group colors for easy comparison

## Data Export

### Excel Export
Click "Export Results" to save data as a multi-sheet Excel workbook containing:
1. **Summary**: Statistical overview of all groups including:
   - Group names and concentrations
   - Peak responses with SEM
   - Time to peak measurements
   - Normalized responses (if enabled)

2. **Individual_Traces**: Complete trace data for each well including:
   - Well IDs and group assignments
   - Concentrations
   - Full time series data

3. **Mean_Traces**: Averaged responses per group including:
   - Time points
   - Mean values
   - SEM calculations

4. **Peak_Responses**: Maximum response data including:
   - Well-by-well peak measurements
   - Time to peak values
   - Group assignments and concentrations

5. **Ionomycin_Normalized**: (When enabled) Normalized response data including:
   - Individual well responses
   - Group statistics
   - Sample IDs and corresponding ionomycin responses

## Tips and Troubleshooting

### Best Practices
1. Load data first before selecting wells
2. Set analysis parameters before processing
3. Use consistent labeling for proper grouping
4. Save layouts for repeated analysis
5. Export results before closing for record keeping

### Common Issues
1. **No plots appearing**:
   - Ensure data is loaded
   - Check well selection
   - Verify analysis parameters

2. **Missing groups in summary**:
   - Check well labels
   - Ensure consistent naming
   - Verify group selection

3. **Artifact removal issues**:
   - Adjust frame parameters
   - Check data alignment
   - Verify timing in raw data

4. **Export problems**:
   - Ensure write permissions in target directory
   - Close any open Excel files
   - Check available disk space

### Support
For additional support or to report issues:
george.dickinson@gmail.com