import logging
import time
from statistics import mean, median, stdev
import csv
import os

s_time = time.time()

logger = logging.getLogger(__name__)


class Analyzer:
    def __init__(self, seq):

        print("Starting preprocessing")
        
        self.sequences = seq
        self.seq_lengths = [len(seq) for seq in self.sequences]
        self.events = flatten(sequences)
        self.items = set(self.events)
        self.number_of_events = len(self.events)
        self.number_of_items = len(self.items)

        print("Creating dictionary")
        self.events_per_item = dict()
        for item in self.items:
            self.events_per_item[item] = 0

        print(f"Counting densities on {len(self.sequences)} sequences")
        self.densities = []
        counter = 0
        print(counter)
        for s in self.sequences:
            counter += 1
            self.densities.append(len(set(s)) / len(s))
            for item in self.items:
                if item in s:
                    self.events_per_item[item] += s.count(item)
        
                    
        print("Finished preprocessing")

    def get_avg_sequence_length(self):
        return mean(self.seq_lengths)

    def get_median_sequence_length(self):
        return median(self.seq_lengths), stdev(self.seq_lengths)

    def get_item_density(self):
        return self.number_of_items / self.number_of_events

    def get_number_of_sequences(self):
        return len(self.sequences)

    def get_avg_number_of_events_per_item(self, ):
        return mean(self.events_per_item.values())
        
    def get_median_number_of_events_per_item(self, ):
        return median(self.events_per_item.values())

    def get_avg_number_of_dist_items_per_sequence(self, ):
        #return self.number_of_items/ self.seq_lengths
        return mean(self.densities)

    def get_median_number_of_dist_items_per_sequence(self, ):
        return median(self.densities), stdev(self.densities)

    def get_density(self):
        return self.get_avg_sequence_length() / self.number_of_items

    def get_density_median(self):
        return self.get_median_sequence_length()[0] / self.number_of_items


def read_input(raw_data):
    with open(raw_data, 'r') as file:
        lines = file.readlines()
    return transform_input(lines)


def flatten(l):
    return [item for sublist in l for item in sublist]


def transform_input(d):
    seq = []
    for sequence in d:
        events_temp = []
        
        for x in sequence.strip().split(" "):
            if x != "-1" and x != "-2":
                events_temp.append(int(x))
        seq.append(events_temp)
    return seq

directory_path = r'PATH TO CONVERTED EVENTLOGS'

# Erstellen Sie eine Liste von Dateipfaden im Verzeichnis
file_input = [os.path.join(directory_path, file) for file in os.listdir(directory_path)]

# Filtern Sie nur Dateien, um Verzeichnisse zu vermeiden
file_input = [file for file in file_input if os.path.isfile(file)]
if file_input:

    header = ['dataset',
              '#sequences',
              '#items',
              '#events',
              'avg_#items_per_seq',
              'median_#items_per_seq',
              'avg_#events_per_item',
              'median_#events_per_item',
              '#items/#events(item_density)',
              'avg_seq_length/#items(density)',
              'median_seq_length/#items(density)'
              ]

    with open('dataset_characteristics.csv', 'w', encoding='UTF8') as out_file:
        writer = csv.writer(out_file)
        # write the header
        writer.writerow(header)
        for in_file in file_input:
            print("##################################\n" +  in_file.split('/')[-1])
            time_s = time.time()
            sequences = read_input(in_file)
            analyzer = Analyzer(sequences)


        
            row = [in_file.split('/')[-1],
                   len(analyzer.sequences),
                   analyzer.number_of_items,
                   analyzer.number_of_events,
                   analyzer.get_avg_number_of_dist_items_per_sequence(),
                   analyzer.get_median_number_of_dist_items_per_sequence(),
                   analyzer.get_avg_number_of_events_per_item(),
                   analyzer.get_median_number_of_events_per_item(),
                   analyzer.get_item_density(),
                   analyzer.get_density(),
                   analyzer.get_density_median()
                   ]

            writer.writerow(row)
            
        print("FINISHED")
