from dataset import Dataset


filepath = 'wine_data_header.csv'
dataset = Dataset(filepath)

# train, test, valid = dataset.datasets_to_sets(10, 10, 50)
#dataset_wine.get_dataset(10,20)
dataset.get_dataset(160,170)
#dataset.dataset_per_class('1')
#dataset.write_to_csv(dataset.data)

#print(dataset)