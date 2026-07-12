from src.analyze import *
from src.visualize import *

if __name__ == '__main__':
    # Analyze
    analyzer = Analyzer()
    analyzer.analyze()
    analyzer.save_main()

    # Visualize
    table = analyzer.get_main_table()
    visualizer = Visualizer(table = table)