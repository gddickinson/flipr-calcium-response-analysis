#!/usr/bin/env python3
"""
PyQtGraph Axis Label Testing Script

This script demonstrates various techniques for handling long axis labels in PyQtGraph.
It creates multiple plots, each demonstrating a different technique.

- Method 1: Line breaks at delimiters
- Method 2: Abbreviated labels with tooltips
- Method 3: Staggered label heights
- Method 4: Custom HTML formatting
- Method 5: Reduced label density
- Method 6: External labels
"""

import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QComboBox, QSpinBox,
    QFormLayout, QGroupBox, QCheckBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import pyqtgraph as pg

# Sample long labels to test with
SAMPLE_LABELS = [
    "ATP | 100 µM | 4026",
    "ATP | 100 µM | 2912",
    "Ionomycin | 1 µM | 4026",
    "Ionomycin | 1 µM | 2912",
    "Buffer | 498",
    "Buffer | 9497"
]

# Create some sample data
def generate_sample_data(num_groups=6):
    """Generate random bar data for testing"""
    np.random.seed(42)  # For reproducibility
    values = np.random.normal(3, 1, num_groups)
    errors = np.random.uniform(0.1, 0.5, num_groups)
    return values, errors

class LabelTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtGraph Axis Label Testing")
        self.resize(1200, 800)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create control panel at top
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)

        # Create tab widget for different test plots
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Add tabs for each method
        self.create_method_tabs()

        # Generate initial data
        self.values, self.errors = generate_sample_data(len(SAMPLE_LABELS))

        # Update all plots
        self.update_all_plots()

    def create_control_panel(self):
        """Create control panel with settings for all plots"""
        panel = QGroupBox("Control Panel")
        layout = QVBoxLayout(panel)

        # Create form layout for controls
        form_layout = QFormLayout()

        # Font size control
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(6, 24)
        self.font_size_spin.setValue(10)
        self.font_size_spin.valueChanged.connect(self.update_all_plots)
        form_layout.addRow("Font Size:", self.font_size_spin)

        # Label length control (simulates making labels longer)
        self.label_length_combo = QComboBox()
        self.label_length_combo.addItems(["Normal", "Longer", "Very Long"])
        self.label_length_combo.currentIndexChanged.connect(self.update_all_plots)
        form_layout.addRow("Label Length:", self.label_length_combo)

        # Number of labels control
        self.num_labels_spin = QSpinBox()
        self.num_labels_spin.setRange(3, 12)
        self.num_labels_spin.setValue(6)
        self.num_labels_spin.valueChanged.connect(self.regenerate_data)
        form_layout.addRow("Number of Labels:", self.num_labels_spin)

        # Add form to layout
        layout.addLayout(form_layout)

        # Add update button
        update_button = QPushButton("Update All Plots")
        update_button.clicked.connect(self.update_all_plots)
        layout.addWidget(update_button)

        return panel

    def create_method_tabs(self):
        """Create tabs for each method"""
        methods = [
            ("Line Breaks", "Split labels at delimiters like '|' with line breaks"),
            ("Abbreviated", "Show shorter labels with full text in tooltips"),
            ("Staggered", "Alternate label positions vertically"),
            ("HTML Formatting", "Format labels with custom HTML/CSS"),
            ("Reduced Density", "Show fewer labels to reduce crowding"),
            ("External Labels", "Place labels below the plot instead of on axis")
        ]

        for name, description in methods:
            tab = QWidget()
            layout = QVBoxLayout(tab)

            # Add description
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

            # Create plot widget
            plot_widget = pg.PlotWidget()
            plot_widget.setBackground('w')
            layout.addWidget(plot_widget)

            # Set tab name as widget property for reference
            plot_widget.setProperty("method_name", name)

            # Store plot widget
            tab.plot_widget = plot_widget

            # Add to tab widget
            self.tab_widget.addTab(tab, name)

    def regenerate_data(self):
        """Regenerate data with current settings"""
        num_labels = self.num_labels_spin.value()
        self.values, self.errors = generate_sample_data(num_labels)
        self.update_all_plots()

    def get_current_labels(self):
        """Get labels with current length setting"""
        length_option = self.label_length_combo.currentText()
        num_labels = self.num_labels_spin.value()

        # Start with base labels
        labels = list(SAMPLE_LABELS)  # Make a copy to avoid modifying the original

        # Extend or create new labels if needed
        while len(labels) < num_labels:
            # Create additional labels based on existing ones
            new_label = f"Sample | {len(labels) + 1} | {np.random.randint(1000, 9999)}"
            labels.append(new_label)

        # Truncate if needed
        labels = labels[:num_labels]

        # Modify label length based on setting
        if length_option == "Longer":
            labels = [f"{label} Extra Text" for label in labels]
        elif length_option == "Very Long":
            labels = [f"{label} With Much Longer Additional Text for Testing" for label in labels]

        return labels

    def update_all_plots(self):
        """Update all plot methods with current settings"""
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            plot_widget = tab.plot_widget
            method_name = plot_widget.property("method_name")

            # Clear the plot
            plot_widget.clear()

            # Apply the appropriate method
            method_func = getattr(self, f"apply_method_{i+1}", self.apply_default_method)
            method_func(plot_widget)

    def create_bar_plot(self, plot_widget, x_labels):
        """Create basic bar plot with the given labels"""
        # Get data
        values = self.values[:len(x_labels)]
        errors = self.errors[:len(x_labels)]
        x = np.arange(len(values))

        # Set axis labels
        plot_widget.setLabel('left', "Value")
        plot_widget.setLabel('bottom', "Group")

        # Set font size
        font_size = self.font_size_spin.value()
        font = QFont()
        font.setPointSize(font_size)

        bottom_axis = plot_widget.getAxis('bottom')
        bottom_axis.setTickFont(font)

        # Create bar chart items
        bar_width = 0.8
        for i, (val, err) in enumerate(zip(values, errors)):
            # Create bar
            bar_item = pg.BarGraphItem(
                x=[i], height=[val], width=bar_width, brush='r'
            )
            plot_widget.addItem(bar_item)

            # Add error bars
            err_item = pg.ErrorBarItem(
                x=np.array([i]), y=np.array([val]),
                height=np.array([err * 2]), beam=0.2,
                pen=pg.mkPen('r', width=2)
            )
            plot_widget.addItem(err_item)

            # Add value label
            label = pg.TextItem(
                text=f'{val:.1f}±{err:.1f}',
                color='r', anchor=(0.5, 1)
            )
            label.setPos(i, val + err)
            plot_widget.addItem(label)

        # Set axis ranges
        plot_widget.setXRange(-0.5, len(values) - 0.5)
        y_max = max(values + errors) * 1.2
        plot_widget.setYRange(0, y_max)

        return x

    def apply_default_method(self, plot_widget):
        """Default method - just creates basic plot with labels"""
        x_labels = self.get_current_labels()
        x = self.create_bar_plot(plot_widget, x_labels)

        # Set tick labels
        bottom_axis = plot_widget.getAxis('bottom')
        bottom_axis.setTicks([[(i, label) for i, label in enumerate(x_labels)]])

    def apply_method_1(self, plot_widget):
        """Method 1: Line breaks at delimiters"""
        x_labels = self.get_current_labels()
        x = self.create_bar_plot(plot_widget, x_labels)

        # Format labels with line breaks
        formatted_labels = []
        for label in x_labels:
            # Split by delimiter if possible
            if '|' in label:
                parts = label.split('|')
                label = '<br>'.join(part.strip() for part in parts)
            elif ' ' in label and len(label) > 15:
                # Split approximately in half at a space
                middle = len(label) // 2
                # Find nearest space to middle
                split_pos = label.rfind(' ', 0, middle)
                if split_pos == -1:
                    split_pos = label.find(' ', middle)
                if split_pos != -1:
                    label = label[:split_pos] + '<br>' + label[split_pos+1:]

            formatted_labels.append(label)

        # Set tick strings
        bottom_axis = plot_widget.getAxis('bottom')

        try:
            # Try to set ticks with HTML formatting
            bottom_axis.setTicks([[(i, formatted_labels[i]) for i in range(len(formatted_labels))]])
        except:
            # If HTML formatting doesn't work, fall back to regular labels
            print("HTML formatting not supported in this PyQtGraph version - using plain text")
            bottom_axis.setTicks([[(i, label.replace('<br>', ' ')) for i, label in enumerate(formatted_labels)]])

    def apply_method_2(self, plot_widget):
        """Method 2: Abbreviated labels with tooltips"""
        x_labels = self.get_current_labels()
        x = self.create_bar_plot(plot_widget, x_labels)

        # Create abbreviated labels
        short_labels = []
        for label in x_labels:
            if '|' in label:
                # Take first part before first pipe
                short_label = label.split('|')[0].strip()
            elif len(label) > 15:
                # Truncate with ellipsis
                short_label = label[:12] + "..."
            else:
                short_label = label

            short_labels.append(short_label)

        # Set tick labels
        bottom_axis = plot_widget.getAxis('bottom')
        bottom_axis.setTicks([[(i, short_label) for i, short_label in enumerate(short_labels)]])

        # Add full labels as small text below (as a substitute for tooltips)
        for i, label in enumerate(x_labels):
            # Add small text in lighter color
            full_text = pg.TextItem(text=label, color=(100, 100, 100), anchor=(0.5, 0))
            font = QFont()
            font.setPointSize(max(6, self.font_size_spin.value() - 2))  # Smaller font
            full_text.setFont(font)
            full_text.setPos(i, -0.2)  # Position below the axis
            plot_widget.addItem(full_text)

    def apply_method_3(self, plot_widget):
        """Method 3: Staggered label heights"""
        x_labels = self.get_current_labels()
        x = self.create_bar_plot(plot_widget, x_labels)

        # Remove default axis labels
        bottom_axis = plot_widget.getAxis('bottom')
        try:
            # Try to hide existing ticks
            bottom_axis.setStyle(tickLength=0)
            # Set empty tick labels
            bottom_axis.setTicks([[(i, "") for i in range(len(x_labels))]])
        except:
            # If that fails, try an alternate approach
            try:
                bottom_axis.setTicks([[]])  # Empty ticks list
            except:
                print("Could not hide default axis labels in Method 3")

        # Create staggered labels
        for i, label in enumerate(x_labels):
            # Alternate positions for even/odd indices
            y_pos = -0.2 if i % 2 == 0 else -0.4

            # Create text item
            text = pg.TextItem(text=label, color='black', anchor=(0.5, 0))
            text.setPos(i, y_pos)
            plot_widget.addItem(text)

        # Expand the view to show all labels
        view_range = plot_widget.viewRange()
        y_min, y_max = view_range[1]
        plot_widget.setYRange(min(-0.6, y_min), y_max)

    def apply_method_4(self, plot_widget):
        """Method 4: Custom HTML formatting"""
        x_labels = self.get_current_labels()
        x = self.create_bar_plot(plot_widget, x_labels)

        # Remove default axis labels
        bottom_axis = plot_widget.getAxis('bottom')
        try:
            # Try to hide existing ticks
            bottom_axis.setStyle(tickLength=0)
            # Set empty tick labels
            bottom_axis.setTicks([[(i, "") for i in range(len(x_labels))]])
        except:
            # If that fails, try an alternate approach
            try:
                bottom_axis.setTicks([[]])  # Empty ticks list
            except:
                print("Could not hide default axis labels in Method 4")

        # Create custom formatted labels
        for i, label in enumerate(x_labels):
            # Create different parts with different formatting
            if '|' in label:
                parts = label.split('|')

                # First part bold
                main_text = pg.TextItem(text=parts[0].strip(), color=(0, 0, 0), anchor=(0.5, 0))
                font = QFont()
                font.setPointSize(self.font_size_spin.value())
                font.setBold(True)
                main_text.setFont(font)
                main_text.setPos(i, -0.15)
                plot_widget.addItem(main_text)

                # Additional parts smaller and lighter
                for j, part in enumerate(parts[1:], 1):
                    sub_text = pg.TextItem(text=part.strip(), color=(100, 100, 100), anchor=(0.5, 0))
                    font = QFont()
                    font.setPointSize(max(6, self.font_size_spin.value() - 2))
                    sub_text.setFont(font)
                    sub_text.setPos(i, -0.15 - (j * 0.1))  # Stack vertically
                    plot_widget.addItem(sub_text)
            else:
                # Just a simple label
                text = pg.TextItem(text=label, color=(0, 0, 0), anchor=(0.5, 0))
                font = QFont()
                font.setPointSize(self.font_size_spin.value())
                text.setFont(font)
                text.setPos(i, -0.15)
                plot_widget.addItem(text)

        # Expand the view to show all labels
        view_range = plot_widget.viewRange()
        y_min, y_max = view_range[1]
        plot_widget.setYRange(min(-0.6, y_min), y_max)

    def apply_method_5(self, plot_widget):
        """Method 5: Reduced label density"""
        x_labels = self.get_current_labels()
        x = self.create_bar_plot(plot_widget, x_labels)

        # Show only a subset of labels to reduce crowding
        bottom_axis = plot_widget.getAxis('bottom')

        # For odd number of labels
        if len(x_labels) % 2 == 1:
            # Show every other label starting with first
            visible_indices = list(range(0, len(x_labels), 2))
        else:
            # Show first, middle and last for even numbers
            if len(x_labels) <= 4:
                visible_indices = [0, len(x_labels)-1]  # Just first and last for 4 or fewer
            else:
                # Show every third label for larger sets
                visible_indices = list(range(0, len(x_labels), 3))
                # Always include first and last
                if visible_indices[-1] != len(x_labels) - 1:
                    visible_indices.append(len(x_labels) - 1)

        # Create tick array with only visible labels
        ticks = []
        for i in range(len(x_labels)):
            if i in visible_indices:
                ticks.append((i, x_labels[i]))
            else:
                ticks.append((i, ""))

        # Set tick marks
        bottom_axis.setTicks([ticks])

        # Add small tick marks for all positions
        for i in range(len(x_labels)):
            # Add a very short line at each tick position
            if i not in visible_indices:
                tick_line = pg.PlotDataItem(
                    [i, i], [0, -0.1],
                    pen=pg.mkPen('black', width=1)
                )
                plot_widget.addItem(tick_line)

    def apply_method_6(self, plot_widget):
        """Method 6: External labels"""
        x_labels = self.get_current_labels()
        x = self.create_bar_plot(plot_widget, x_labels)

        # Hide axis labels completely
        bottom_axis = plot_widget.getAxis('bottom')
        try:
            # Try to hide existing ticks
            bottom_axis.setStyle(tickLength=0)
            # Set empty tick labels
            bottom_axis.setTicks([[(i, "") for i in range(len(x_labels))]])
        except:
            # If that fails, try an alternate approach
            try:
                bottom_axis.setTicks([[]])  # Empty ticks list
            except:
                print("Could not hide default axis labels in Method 6")

        # Add vertical lines at each position
        for i in range(len(x_labels)):
            line = pg.InfiniteLine(pos=i, angle=90, pen=pg.mkPen('gray', width=0.5, style=Qt.DotLine))
            plot_widget.addItem(line)

        # Create separate label container below the plot
        font_size = self.font_size_spin.value()

        # Calculate positions with equal spacing
        for i, label in enumerate(x_labels):
            # Create text below the axis
            text = pg.TextItem(text=label, anchor=(0.5, 0))
            text.setPos(i, -0.5)

            # Set font
            font = QFont()
            font.setPointSize(font_size)
            text.setFont(font)

            plot_widget.addItem(text)

        # Adjust bottom margin to make room for labels
        # Get the current view range
        view_range = plot_widget.viewRange()
        y_min, y_max = view_range[1]

        # Fix: Set the Y range with explicit values instead of using None
        plot_widget.setYRange(min(-1.5, y_min), y_max)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabelTestApp()
    window.show()
    sys.exit(app.exec_())
