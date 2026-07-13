from src.analyze import *
from src.visualize import *

if __name__ == '__main__':
    # Analyze
    analyzer = Analyzer()
    analyzer.analyze()
    analyzer.save_main()
    analyzer.save_aggregation(column = 'price')
    analyzer.save_correlation()

    # Visualize
    table = analyzer.get_main()
    visualizer = Visualizer(table = table)