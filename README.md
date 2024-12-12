# FLIPR Analysis Tool User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Main Interface](#main-interface)
5. [Loading Data](#loading-data)
6. [Plate Layout Configuration](#plate-layout-configuration)
7. [Data Analysis](#data-analysis)
8. [Visualization](#visualization)
9. [Exporting Results](#exporting-results)
10. [Troubleshooting](#troubleshooting)

## Introduction

The FLIPR Analysis Tool is a specialized software application designed for analyzing calcium imaging data from FLIPR (Fluorometric Imaging Plate Reader) experiments. It provides a comprehensive suite of tools for data processing, visualization, and analysis of calcium responses in 96-well plate formats.

### Key Features
- Interactive 96-well plate layout configuration
- Raw and ΔF/F₀ trace visualization
- Automated artifact removal
- Statistical analysis with multiple metrics
- Ionomycin normalization capability
- Comprehensive data export options
- Area Under Curve (AUC) analysis
- Time to peak measurements

## Installation

### System Requirements
- Python 3.9 or later
- Required libraries:
  - PyQt5
  - pandas
  - numpy
  - pyqtgraph
  - openpyxl

### Installation Steps
1. Install Python from https://www.python.org/downloads/
2. Install required packages using pip:
```bash
pip install PyQt5 pandas numpy pyqtgraph openpyxl
```
3. Download and run the FLIPR Analysis Tool script

## Getting Started

### Initial Setup
1. Launch the application
2. Configure analysis parameters (Analysis → Parameters)
3. Load your FLIPR data file
4. Configure your plate layout before analysis

### File Formats
The tool accepts FLIPR output files in the following formats:
- .seq1 files (FLIPR native format)
- Tab-delimited text files (.txt)
- File must contain a header row and time-series data

## Main Interface

### Window Layout
The interface consists of two main tabs:
1. **Plate Layout Tab**
   - 96-well plate grid
   - Well labeling controls
   - Mode selection
   - Action buttons

2. **Analysis Tab**
   - Plot controls
   - Analysis parameters
   - Results display
   - Export options

### Menu Bar
- **File**: Layout export options
- **Analysis**: Parameter settings
- **Help**: Manual and about information

## Loading Data

### Loading a Data File
1. Click "Load Data" or use File → Open
2. Select your .seq1 or .txt file
3. The file will be validated and loaded
4. A confirmation message will appear upon successful loading

### Data Validation
The tool automatically checks for:
- Correct file format
- Complete header information
- Valid numerical data
- Appropriate number of columns

## Plate Layout Configuration

### Well Selection
- Click individual wells to select/deselect
- Click row headers (A-H) to select entire rows
- Click column headers (1-12) to select entire columns
- Click top-left corner to select all wells

### Labeling Modes
1. **Simple Label**
   - Enter agonist name
   - Enter concentration
   - Enter sample ID
   - Choose color
   - Apply to selected wells

2. **Log10 Series**
   - Enter starting concentration
   - Select multiple wells in order
   - System calculates dilution series

3. **Clear Wells**
   - Removes all labels from selected wells

### Color Coding
- Click color button to open color picker
- Colors help visualize different conditions
- Colors are preserved in plots and exports

## Data Analysis

### Analysis Parameters
Access via Analysis → Parameters to set:
- Artifact Start Frame: Beginning of injection artifact
- Artifact End Frame: End of injection artifact
- Baseline Frames: Number of frames for F₀ calculation
- Peak Start Frame: Frame to begin peak detection

### Processing Options
1. **Artifact Removal**
   - Toggle "Remove Injection Artifact"
   - Automatically removes specified frames
   - Updates all calculations and plots

2. **Ionomycin Normalization**
   - Toggle "Normalize to Ionomycin"
   - Normalizes responses to ionomycin control
   - Groups by sample ID

3. **Area Under Curve**
   - Automatically calculated for all traces
   - Displayed in summary plots and exports
   - Uses trapezoidal integration

4. **Time to Peak**
   - Calculated from start of response
   - Accounts for artifact removal if enabled
   - Shown in summary plots and exports

## Visualization

### Available Plot Types
1. **Raw Traces**
   - Shows raw intensity values
   - Individual well traces
   - Color-coded by group

2. **ΔF/F₀ Traces**
   - Normalized calcium responses
   - Baseline-corrected
   - Color-coded by group

3. **Summary Plots**
   - Individual Traces: All responses by group
   - Mean Traces: Average with SEM
   - Peak Responses: Bar graphs with error bars
   - Area Under Curve: AUC comparison
   - Time to Peak: Response timing
   - Normalized (when enabled): % of ionomycin

### Plot Controls
- Toggle grid display
- Clear individual plots
- Show/hide legend
- Export plots as images

## Exporting Results

### Excel Export
Creates a workbook with multiple sheets:
1. **Summary**
   - Group statistics
   - Peak responses
   - AUC values
   - Time to peak
   - Normalized responses (if enabled)

2. **Individual_Traces**
   - Complete trace data
   - Well assignments
   - Concentrations

3. **Mean_Traces**
   - Averaged responses
   - SEM calculations
   - Time points

4. **Peak_Responses**
   - Maximum responses
   - Time to peak
   - AUC values

5. **Analysis_Metrics**
   - Detailed statistics
   - Group comparisons
   - Quality metrics

### FLIPR Format Export
- Exports plate layout as .fmg file
- Compatible with FLIPR software
- Preserves groups and colors

## Troubleshooting

### Common Issues

1. **Data Loading Problems**
   - Check file format
   - Verify data structure
   - Ensure no missing values

2. **Plot Display Issues**
   - Verify well selection
   - Check data processing
   - Confirm parameter settings

3. **Export Errors**
   - Check file permissions
   - Close existing Excel files
   - Verify available disk space

### Error Messages
- Detailed error messages in status bar
- Log file for debugging
- Contact support for assistance

### Support
For additional support or to report issues:
[george.dickinson@gmail.com]

## Tips and Best Practices

1. **Data Organization**
   - Label wells before analysis
   - Use consistent naming
   - Save layouts for repeated experiments

2. **Analysis Workflow**
   - Set parameters first
   - Verify well assignments
   - Review raw data before processing

3. **Quality Control**
   - Check baseline stability
   - Verify artifact removal
   - Compare replicates

4. **Data Export**
   - Save layouts separately
   - Document parameter settings
   - Include all relevant metadata
