import csv
import random


class Dataset:

    def __init__(self, datasource):
        self.datasource = datasource
        self.data, self.headers = self.load_dataset()
        #self.train, self.test, self.valid = self.datasets_to_sets()

    def check_headers(self, source):
        csv_test_bytes = source.read(1024)  # Grab a sample of the CSV for format detection
        source.seek(0)  # Rewind
        has_header = csv.Sniffer().has_header(csv_test_bytes)  # Check to see if there's a header in the file
        return has_header

    def load_dataset(self):
        with open(filepath, newline='') as source:
            has_header = self.check_headers(source)

            reader = csv.reader(source)
            headers_list = next(reader)
            dataset_list = list(reader)

            if has_header:
                return dataset_list, headers_list
            else:
                return dataset_list, ['Headers did not appear in this dataset.']

    def get_labels(self):
        for elem in self.headers:
            print(elem)

    def get_dataset(self, *args):
        if args:
            start, stop = args
        else:
            start = 0
            stop = len(self.data)

        for row in self.data[start:stop]:
            print(*row, sep=', ')

    def datasets_to_sets(self, training=100, test=100, validation=100):
        training_set = random.sample(self.data, int(len(self.data) * training/100))
        test_set = random.sample(self.data, int(len(self.data) * test/100))
        validation_set = random.sample(self.data, int(len(self.data) * validation / 100))

        return training_set, test_set, validation_set

    def decision_classes(self, printIt = True):
        class_names = []
        n = 0
        for elem in self.data:
            if elem[0] not in class_names:
                class_names.append(elem[0])

        classes_count = {item: 0 for item in class_names}

        while n < len(class_names):
            for elem in self.data:
                if elem[0] == class_names[n]:
                    classes_count[class_names[n]] += 1
            n += 1

        for key, value in classes_count.items():
            if printIt:
                print((key, value))
        return class_names

    def dataset_per_class(self, decision_class):
        decision_classes = self.decision_classes(printIt=False)
        print(decision_classes)
        new_data = []
        if decision_class in decision_classes:
            for elem in self.data:
                if elem[0] == str(decision_class):
                    new_data.append(elem)
        else:
            print(f'Class you have provided: "{decision_class}" does not exist in dataset.')
        for row in new_data:
            print(*row, sep=', ')

    def write_to_csv(self, param):
        target_data = 'wine_output.csv'
        headers = self.headers
        with open(target_data, 'w', newline='') as f:
            writer = csv.writer(f)
            if len(headers)>1:
                writer.writerow(headers)
            writer.writerows(param)




filepath = 'wine_data_header.csv'
#filepath = 'wine_data.csv'

dataset_wine = Dataset(filepath)

#print(dataset_wine.load_dataset())
#dataset_wine.get_dataset(10,20)
dataset_wine.get_labels()
#print(dataset_wine.datasets_to_sets(2,2, 2))

#dataset_wine.decision_classes()
#dataset_wine.dataset_per_class('3')

train, test, valid = dataset_wine.datasets_to_sets(10, 10, 50)
#dataset_wine.write_to_csv(dataset_wine.datasets_to_sets(10,15,19)[2])
#dataset_wine.write_to_csv(train)


