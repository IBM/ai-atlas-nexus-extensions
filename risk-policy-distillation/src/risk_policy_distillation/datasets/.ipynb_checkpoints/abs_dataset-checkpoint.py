import configparser
import logging
import os
import numpy as np
import pandas as pd
from datasets import load_dataset, DatasetDict

logger = logging.getLogger('logger')


class AbstractDataset:
    # TODO: allow config to have default parameters

    def __init__(self, config, dataframe=None):
        self.process_config(config)

        if dataframe is None:
            try:
                dataframe = load_dataset(self.location)
                dataframe = dataframe.data[self.subset].table.to_pandas()
                dataframe = dataframe.sample(int(len(dataframe)*self.sample_ratio))
                logger.info(f'Loaded dataset with {len(dataframe)} instances.)')
            except KeyError:
                print('Either dataframe or valid dataset name have to be provided for Dataset initialization.')

        self.dataframe = self.preprocess_df(dataframe, config)

        if self.split:
            # load dataset
            try:
                self.train, self.val, self.test = [pd.read_csv(os.path.join(f'datasets/{self.dataset_name}', f'{split}.csv')) for split in ['train', 'val', 'test']]
                logger.info(f'Loaded datasets from datasets/{self.dataset_name}')
            except FileNotFoundError:
                self.train, self.val, self.test = self.split_df(self.dataframe, [0.6, 0.2, 0.2])

                dataset_path = os.path.join('datasets', self.dataset_name)
                if not os.path.isdir(dataset_path):
                    os.makedirs(dataset_path)

                self.train.to_csv(os.path.join(dataset_path, 'train.csv'), index_label='Index')
                self.val.to_csv(os.path.join(dataset_path, 'val.csv'), index_label='Index')
                self.test.to_csv(os.path.join(dataset_path, 'test.csv'), index_label='Index')

                logger.info('Dataset split into train = {} instances, val = {} instances and '
                            'test = {} instances.'.format(len(self.train), len(self.val), len(self.test)))
        else:
            try:
                self.train = pd.read_csv(os.path.join(f'datasets/{self.dataset_name}', 'train.csv'))
                self.val = self.train
                self.test = self.train
            except FileNotFoundError:
                self.train = self.dataframe
                self.val = self.dataframe
                self.test = self.dataframe

                print('here!')

                dataset_path = os.path.join('datasets', self.dataset_name)
                if not os.path.isdir(dataset_path):
                    os.makedirs(dataset_path)

                self.train.to_csv(os.path.join(dataset_path, 'train.csv'), index_label='Index')
                logger.info(f'Saved the entire dataset as train to datasets/{self.dataset_name}/train.csv')

    def process_config(self, c):
        # TODO: verify all columns are passed and exist in the dataframe
        config = configparser.ConfigParser()

        config.read_dict(c)

        self.dataset_name = config.get('general', 'dataset_name')
        try:
            self.location = config.get("general", 'location')
        except configparser.NoOptionError:
            self.location = None
            print('Warning: No download location provided for the dataset')

        self.index_col = config.get('data', 'index_col')
        self.prompt_col = config.get('data', 'prompt_col')
        self.label_col = config.get('data', 'label_col')
        self.flip_labels = config.getboolean('data', 'flip_labels')
        self.split = config.getboolean('split', 'split')

        if self.location is not None: # if loading from huggingface need to know which split is used
            self.subset = config.get('split', 'subset')
            self.sample_ratio = config.getfloat('split', 'sample_ratio')

    def size(self):
        if self.dataframe is None:
            return 0

        return len(self.dataframe)

    def preprocess_df(self, dataframe, config):
        if isinstance(dataframe, DatasetDict):
            assert self.split is not None
            dataframe = dataframe.data[self.subset].table.to_pandas()

        if self.index_col == '':
            dataframe['Index'] = np.arange(0, len(dataframe))
            dataframe = dataframe.rename(columns={self.index_col: 'Index'})
            self.index_col = 'Index'

        if self.label_col == '':
            dataframe['label'] = [1] * len(dataframe)
            dataframe = dataframe.rename(columns={self.label_col: 'label'})
            self.label_col = 'label'

        if self.flip_labels:
            dataframe[self.label_col] = 1 - dataframe[self.label_col]

        if self.sample_ratio is not None:
            dataframe = dataframe.sample(int(len(dataframe)*self.sample_ratio))

        return dataframe

    def extract_message(self, row):
        pass

    def split_df(self, dataset, ratios):
        dataset = dataset.sample(frac=1, random_state=42)

        start = 0
        datasets = []
        for r in ratios:  # Shuffle the DataFrame
            size = int(len(dataset) * r)
            d = dataset.iloc[start:(start + size)]
            start = start + size

            datasets.append(d)

        return datasets

