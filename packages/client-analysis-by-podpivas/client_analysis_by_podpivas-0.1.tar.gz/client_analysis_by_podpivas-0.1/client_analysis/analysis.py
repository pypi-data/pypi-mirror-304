import pandas as pd


class ClientAnalysis:
    def __init__(self, input_file):
        self.data = pd.read_csv(input_file)

    def total_clients(self):
        return len(self.data)

    def age_distribution(self):
        age_bins = [18, 25, 35, 45, 60, 100]
        age_labels = ['18-25', '26-35', '36-45', '46-60', '60+']
        self.data['Age Group'] = pd.cut(self.data['age'], bins=age_bins, labels=age_labels, right=False)
        return self.data['Age Group'].value_counts()

    def city_distribution(self):
        return self.data['city'].value_counts()
