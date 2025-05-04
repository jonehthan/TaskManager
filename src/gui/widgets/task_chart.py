import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from datetime import datetime


class TaskChart:
    def __init__(self, parent, tasks):
        self.parent = parent
        self.tasks = tasks

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
        ax1.set_title('Task Completion Rate')

        # Daily completion bar chart
        ax2 = fig.add_subplot(122)
        daily_stats = self._get_daily_stats()
        ax2.bar(daily_stats.keys(), daily_stats.values())
        ax2.set_title('Daily Completions')
        ax2.tick_params(axis='x', rotation=45)

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
