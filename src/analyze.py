import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

class Analyzer:
    # How much should price affect the final rating | range = [0, 1]
    price_weight = 0.25

    def __init__(self):
        self.engine = create_engine(f'postgresql+psycopg://postgres:1qaz2wsx@localhost:5432/smartphones')
        self.table = pd.read_sql('''
                                 SELECT
                                    phones.*,
                                    dict_brands.brand_name
                                 FROM phones
                                 JOIN dict_brands
                                 ON phones.brand_id = dict_brands.id
                                 ''',
                                 self.engine)
        self.original_columns = self.table.columns.to_list()

    def analyze(self):
        self.insert_ppi()
        self.insert_price_per_unit()
        self.fill_null()
        self.bool_to_int()
        self.normalize()
        self.insert_overall_score()
        self.sort_by_pricevalue()
    
    def insert_ppi(self):
        self.table['resolution_width'] = self.table['resolution'].str[0]
        self.table['resolution_height'] = self.table['resolution'].str[1]
        screen_size_pixels = np.sqrt(self.table['resolution_width']**2 + self.table['resolution_height']**2)
        self.table['ppi'] = screen_size_pixels / self.table['screen_size']

    def insert_price_per_unit(self):
        self.table['price_per_battery'] = self.table['price'] / self.table['battery_capacity']
        self.table['price_per_ram'] = self.table['price'] / self.table['ram_capacity']
        self.table['price_per_camera'] = self.table['price'] / self.table['primary_camera_rear']

    def fill_null(self):
        fill_zero = ['has_5g', 'has_nfc', 'has_ir_blaster', 'fast_charging', 'extended_upto']
        fill_median = ['rating', 'processor_speed', 'battery_capacity', 'ram_capacity',
                       'internal_memory', 'refresh_rate', 'primary_camera_rear', 'primary_camera_front', 'ppi']
        
        self.table[fill_zero] = self.table[fill_zero].fillna(0)
        self.table[fill_median] = self.table[fill_median].apply(
            lambda col: col.fillna(col.median())
        )
    
    def bool_to_int(self):
        bool_cols = ['has_5g', 'has_nfc', 'has_ir_blaster']
        self.table[bool_cols] = self.table[bool_cols].astype(int)

    def normalize(self):
        cols = ['price', 'rating', 'processor_speed', 'battery_capacity', 'fast_charging', 'ram_capacity',
                'internal_memory', 'refresh_rate', 'primary_camera_rear', 'primary_camera_front',
                'extended_upto', 'ppi']
        normalized_cols = [col + '_normalized' for col in cols]
        scaler = MinMaxScaler()
        self.table[normalized_cols] = scaler.fit_transform(self.table[cols])

    def insert_overall_score(self):
        self.table['value_score'] = Analyzer.calc_valuescore(table = self.table)
        self.table['price_value'] = Analyzer.calc_pricevalue(table = self.table)

    @staticmethod
    def calc_valuescore(table):
        coeffs = {
            'rating_normalized': 0.2,
            'has_5g': 0.02,
            'has_nfc': 0.02,
            'has_ir_blaster': 0.01,
            'processor_speed_normalized': 0.15,
            'battery_capacity_normalized': 0.08,
            'fast_charging_normalized': 0.03,
            'ram_capacity_normalized': 0.15,
            'internal_memory_normalized': 0.15,
            'refresh_rate_normalized': 0.04,
            'primary_camera_rear_normalized': 0.08,
            'primary_camera_front_normalized': 0.01,
            'extended_upto_normalized': 0.01,
            'ppi_normalized': 0.05
        }

        value_score = sum(table[col] * coeff for col, coeff in coeffs.items())
        return value_score

    @classmethod
    def calc_pricevalue(cls, table):
        value_score_weight = 1 - cls.price_weight
        visibility_factor = 10**3
        
        price_value = (table['value_score'] * value_score_weight) + ( (1 - table['price_normalized']) * cls.price_weight )
        price_value *= visibility_factor
        price_value = round(price_value, 2)

        return price_value

    def sort_by_pricevalue(self):
        self.table.sort_values('price_value', ascending = False, inplace = True)

    def get_main_table(self):
        return self.table

    def get_correlation(self):
        corr_cols = ['price', 'battery_capacity', 'ram_capacity', 'internal_memory',
                     'num_rear_cameras', 'num_front_cameras', 'primary_camera_rear',
                     'primary_camera_front']
        corr = self.table[corr_cols].corr()
        corr_price = corr['price'].sort_values(ascending = False)

        return corr_price
    
    def get_avg_price_by_column(self, column_name):
        avg = self.table.groupby(column_name)['price'].mean().reset_index(name = 'average_price')

        return avg
    
    def save(self, table):
        columns = self.original_columns + ['price_value']
        table[columns].to_csv(Path('csv') / 'result.csv', index = False)