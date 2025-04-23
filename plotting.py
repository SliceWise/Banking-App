"""
Plotting module for the Banking Application
Handles data visualization and chart generation
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import os

# Create plots directory if it doesn't exist
os.makedirs('data/plots', exist_ok=True)

def pie_chart(labels, values, title):
    """Create a pie chart with the given labels, values, and title"""
    try:
        # Filter out zero values and their corresponding labels
        non_zero_values = []
        non_zero_labels = []
        for i in range(len(values)):
            if values[i] > 0:
                non_zero_values.append(values[i])
                non_zero_labels.append(labels[i])
        
        if not non_zero_values:
            print("No data to plot.")
            return False
        
        # Create the pie chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(non_zero_values, labels=non_zero_labels, autopct='%1.1f%%', 
               shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        plt.title(title)
        plt.tight_layout()
        
        # Display the chart
        plt.show()
        
        # Save the chart
        filename = f"data/plots/{title.lower().replace(' ', '_')}.png"
        plt.savefig(filename)
        plt.close()
        
        print(f"\nChart saved as {filename}")
        return True
    except Exception as e:
        print(f"Error creating pie chart: {e}")
        return False

def bar_chart(labels, values, title):
    """Create a bar chart with the given labels, values, and title"""
    try:
        if not values:
            print("No data to plot.")
            return False
        
        # Create the bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(labels))
        
        bars = ax.bar(x, values, width=0.6)
        
        # Add value labels on top of each bar
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'${height:.2f}', ha='center', va='bottom')
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel('Amount ($)')
        ax.set_title(title)
        
        plt.tight_layout()
        
        # Display the chart
        plt.show()
        
        # Save the chart
        filename = f"data/plots/{title.lower().replace(' ', '_')}.png"
        plt.savefig(filename)
        plt.close()
        
        print(f"\nChart saved as {filename}")
        return True
    except Exception as e:
        print(f"Error creating bar chart: {e}")
        return False

def line_chart(labels, data_series, series_names, title):
    """Create a line chart with multiple data series"""
    try:
        if not data_series or not any(data_series):
            print("No data to plot.")
            return False
        
        # Create the line chart
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(labels))
        
        for i, data in enumerate(data_series):
            ax.plot(x, data, marker='o', linestyle='-', label=series_names[i])
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel('Amount ($)')
        ax.set_title(title)
        ax.legend()
        
        # Add grid lines
        ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Display the chart
        plt.show()
        
        # Save the chart
        filename = f"data/plots/{title.lower().replace(' ', '_')}.png"
        plt.savefig(filename)
        plt.close()
        
        print(f"\nChart saved as {filename}")
        return True
    except Exception as e:
        print(f"Error creating line chart: {e}")
        return False

def stacked_bar_chart(labels, data_series, series_names, title):
    """Create a stacked bar chart with multiple data series"""
    try:
        if not data_series or not any(data_series):
            print("No data to plot.")
            return False
        
        # Create the stacked bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(labels))
        
        bottom = np.zeros(len(labels))
        for i, data in enumerate(data_series):
            ax.bar(x, data, bottom=bottom, label=series_names[i])
            bottom += np.array(data)
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel('Amount ($)')
        ax.set_title(title)
        ax.legend()
        
        plt.tight_layout()
        
        # Display the chart
        plt.show()
        
        # Save the chart
        filename = f"data/plots/{title.lower().replace(' ', '_')}.png"
        plt.savefig(filename)
        plt.close()
        
        print(f"\nChart saved as {filename}")
        return True
    except Exception as e:
        print(f"Error creating stacked bar chart: {e}")
        return False

def check_matplotlib():
    """Check if matplotlib is installed and available"""
    try:
        import matplotlib
        return True
    except ImportError:
        print("\nMatplotlib is not installed. Please install it for data visualization:")
        print("pip install matplotlib")
        return False
