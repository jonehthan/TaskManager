import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

class TaskChart:
    def __init__(self, parent, tasks):
        self.parent = parent
        self.tasks = tasks
        self.days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def plot_completion_charts(self):
        """Create and display task completion charts"""
        # Create completion stats
        completed = len([t for t in self.tasks if t.status == "Completed"])
        total = len(self.tasks)
        completion_rate = (completed / total * 100) if total > 0 else 0

        # Create figure
        fig = Figure(figsize=(10, 5))

        # Progress pie chart
        ax1 = fig.add_subplot(121)
        ax1.pie([completion_rate, 100 - completion_rate],
                labels=['Completed', 'Pending'],
                colors=['#4CAF50', '#FFC107'],
                autopct='%1.1f%%')
        ax1.set_title('Tasks Progress')

        # Daily completion bar chart
        ax2 = fig.add_subplot(122)
        daily_stats = self._get_daily_stats()

        # Create list of values for all days of the week
        values = [daily_stats.get(day, 0) for day in self.days_of_week]

        ax2.bar(self.days_of_week, values, color='#4CAF50')
        ax2.set_title('Completed Tasks by Day of the Week')
        
        ax2.set_xlabel('Day of the Week')
        ax2.set_ylabel('Number of Completed Tasks')

        # Set x-axis rotation and y-axis properties
        ax2.tick_params(axis='x', rotation=45)

        # Set y-axis to start at 0 and increment by 1
        max_value = max(values) if values else 1
        ax2.set_ylim(0, max_value + 1)
        ax2.yaxis.set_major_locator(plt.MultipleLocator(1))

        # Add grid lines for better readability
        ax2.grid(True, axis='y', linestyle='--', alpha=0.7)

        # Adjust layout to prevent label cutoff
        fig.tight_layout()

        # Create canvas and display
        canvas = FigureCanvasTkAgg(fig, self.parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _get_daily_stats(self):
        """Calculate daily completion statistics"""
        daily_counts = Counter()
        for task in self.tasks:
            if task.status == "Completed" and task.completed_date:
                day = task.completed_date.strftime('%A')
                daily_counts[day] += 1
        return daily_counts