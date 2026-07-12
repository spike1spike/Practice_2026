import pandas as pd

class Converter:
    def __init__(self):
        columns_to_int = ['rating', 'num_cores', 'battery_capacity', 'fast_charging', 'ram_capacity', \
                          'internal_memory', 'num_front_cameras', 'extended_upto']
        columns_to_bool = ['fast_charging_available', 'extended_memory_available']

        self.table = pd.read_csv('database_original.csv')
        for column in columns_to_int:
            self.table[column] = self.table[column].apply(self.to_int).astype('Int64')
        for column in columns_to_bool:
            self.table[column] = self.table[column].apply(self.to_bool)
    
    @staticmethod
    def to_int(value):
        if pd.isna(value): return value

        if value.is_integer():
            return int(value)
        else:
            raise ValueError('UNABLE TO CONVERT A VALUE')

    @staticmethod
    def to_bool(value):
        if pd.isna(value): return value

        if value in (0, 1):
            return bool(value)
        else:
            raise ValueError('UNABLE TO CONVERT A VALUE')
    
    def save(self):
        self.table.to_csv('database_edited.csv', index = False)

if __name__ == '__main__':
    converter = Converter()
    converter.save()