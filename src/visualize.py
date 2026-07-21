import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self, table):
        self.table = table
        self.insert_top_brand_name()

    def insert_top_brand_name(self):
        top_brands = self.table['brand_name'].value_counts().head(5).index
        self.table['top_brand_name'] = self.table['brand_name'].where(self.table['brand_name'].isin(top_brands),
                                                                      'OTHER')

    def create_pairplot_all(self):
        features = [
            'price',
            'rating',
            'processor_speed',
            'ram_capacity',
            'value_score',
        ]

        sns.pairplot(self.table,
                     vars = features,
                     hue = 'top_brand_name',
                     diag_kind = 'hist',
                     corner = True)
        plt.show()
    
    def create_scatter_ramcapacity(self):
        sns.scatterplot(self.table,
                        x = 'price',
                        y = 'ram_capacity',
                        hue = 'top_brand_name')
        plt.show()
    
    def create_scatter_internalmemory(self):
        sns.scatterplot(self.table,
                        x = 'price',
                        y = 'internal_memory',
                        hue = 'top_brand_name')
        plt.show()
    
    def create_boxplot_brands(self):
        sns.boxplot(self.table,
                    x = 'price',
                    y = 'brand_name')
        plt.show()