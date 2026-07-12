from src.analyze import *
from src.visualize import *

if __name__ == '__main__':
    # Analyze
    analyzer = Analyzer()
    analyzer.analyze()
    table = analyzer.get_main_table()
    analyzer.save(table = table)

    # Visualize
    visualizer = Visualizer(table = table)
    visualizer.create_boxplot_brands()