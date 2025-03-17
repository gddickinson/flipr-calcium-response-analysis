# FLIPR Analysis Tool User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Main Interface](#main-interface)
5. [Loading Data](#loading-data)
6. [Plate Layout Configuration](#plate-layout-configuration)
7. [Data Analysis](#data-analysis)
8. [Experiment Metadata](#experiment-metadata)
9. [Visualization](#visualization)
10. [Exporting Results](#exporting-results)
11. [Troubleshooting](#troubleshooting)

## Introduction

The FLIPR Analysis Tool is a specialized software application designed for analyzing calcium imaging data from FLIPR (Fluorometric Imaging Plate Reader) experiments. It provides a comprehensive suite of tools for data processing, visualization, and analysis of calcium responses in 96-well plate formats.

### Key Features
- Interactive 96-well plate layout configuration
- Direct CSV layout import from FLIPR machine outputs
- Raw and ΔF/F₀ trace visualization
- Automated artifact removal
- Statistical analysis with multiple metrics
- Ionomycin normalization capability
- Comprehensive data export options with experiment metadata
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
5. Enter experiment metadata for comprehensive exports

### File Formats
The tool accepts FLIPR output files in the following formats:
- .seq1 files (FLIPR native format)
- Tab-delimited text files (.txt)
- CSV files for plate layout import
- File must contain a header row and time-series data

## Main Interface

### Window Layout
The interface consists of three main tabs:
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

3. **Experiment Metadata Tab**
   - Experiment details input
   - Template saving/loading
   - Sample-specific documentation

### Menu Bar
- **File**: Layout export/import options, metadata templates
- **Analysis**: Parameter settings
- **Help**: Manual and about information

## Loading Data

### Loading a Data File
1. Click "Load Data" or use File → Open
2. Select your .seq1 or .txt file
3. The file will be validated and loaded
4. A confirmation message will appear upon successful loading

### Loading Plate Layout from CSV
1. Click "Load CSV Layout" or use File → Load CSV Layout
2. Select your CSV file exported from the FLIPR machine
3. The application will extract well IDs and group names
4. Wells will be automatically labeled and color-coded

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

## Experiment Metadata

### Metadata Entry
The Experiment Metadata tab allows you to enter detailed information about your experiment:
- Accession ID
- Aliquot
- Plate per run date
- Passage number
- Objective
- Experiment date
- Media type
- FBS lot number
- Cell density
- Time frame
- Variables
- Lab operator
- Phenotype
- Results of interest
- Expected/optimal results

### Metadata Templates
- Save metadata as templates for repeated experiments
- Load templates to quickly populate fields
- Templates are stored as JSON files for easy sharing

### Integration with Sample IDs
- Sample IDs are defined in the plate layout
- Each unique Sample ID gets its own row in the experiment summary
- Measurements are calculated separately for each Sample ID

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

2. **Experiment Summary**
   - Complete experiment metadata
   - Sample-specific measurements
   - Organized by unique Sample IDs
   - Direct comparison of ATP, Ionomycin, and HBSS responses
   - Normalized responses for each Sample ID

3. **Individual_Traces**
   - Complete trace data
   - Well assignments
   - Concentrations

4. **Mean_Traces**
   - Averaged responses
   - SEM calculations
   - Time points

5. **Peak_Responses**
   - Maximum responses
   - Time to peak
   - AUC values

6. **Analysis_Metrics**
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

2. **CSV Layout Import Issues**
   - Verify the CSV contains "Group Name" and "Well ID" columns
   - Check that well IDs are in correct format (e.g., "A1", "B2")
   - Ensure group names are properly aligned with well IDs

3. **Plot Display Issues**
   - Verify well selection
   - Check data processing
   - Confirm parameter settings

4. **Export Errors**
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
   - Use Sample IDs consistently for proper grouping in exports

2. **CSV Layout Import**
   - Export CSV directly from FLIPR machine when possible
   - Review group assignments after import
   - Adjust colors manually if needed

3. **Using Metadata**
   - Create templates for common experiment types
   - Be consistent with Sample IDs between plate layout and metadata
   - Fill in all relevant fields for comprehensive documentation

4. **Analysis Workflow**
   - Set parameters first
   - Verify well assignments
   - Review raw data before processing
   - Enter metadata before exporting results

5. **Quality Control**
   - Check baseline stability
   - Verify artifact removal
   - Compare replicates

6. **Data Export**
   - Save layouts separately
   - Document parameter settings
   - Include all relevant metadata
   - Name files consistently for easy tracking
