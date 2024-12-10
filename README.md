# FLIPR Analysis Tool User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Main Interface](#main-interface)
4. [Data Loading and Processing](#data-loading-and-processing)
5. [Well Selection and Labeling](#well-selection-and-labeling)
6. [Analysis Features](#analysis-features)
7. [Visualization Options](#visualization-options)
8. [Tips and Troubleshooting](#tips-and-troubleshooting)

## Introduction
The FLIPR Analysis Tool is designed for analyzing calcium imaging data from FLIPR experiments. It provides an intuitive interface for data processing, visualization, and analysis of calcium responses in 96-well plate formats.

## Getting Started

### System Requirements
- Python 3.x
- Required libraries: PyQt5, pyqtgraph, pandas, numpy
- Sufficient memory to handle FLIPR data files

### Data Format
The tool accepts FLIPR output files (.seq1) with the following characteristics:
- Tab-delimited text format
- Metadata in the first column
- Raw time series intensity values from column 5 onwards
- First row containing header values

## Main Interface

### Layout Components
1. **Well Plate Grid**: 96-well plate representation
2. **Control Panel**: Data loading and analysis options
3. **Plot Windows**: Various data visualization options

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
   - Enter concentration
   - Enter sample ID
   - Select color (optional)
   - Click "Apply Label"

2. **Log10 Series**:
   - Enter starting concentration
   - Select multiple wells
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
Three tabs available:
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
   - Excludes ionomycin group

## Tips and Troubleshooting

### Best Practices
1. Load data first before selecting wells
2. Set analysis parameters before processing
3. Use consistent labeling for proper grouping
4. Save layouts for repeated analysis

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

### Support
For additional support or to report issues:
george.dickinson@gmail.com
