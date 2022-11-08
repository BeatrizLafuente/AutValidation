from typing import Dict, Iterable, List
import regex as re
import pandas as pd
from allennlp.data import DatasetReader, Instance
from allennlp.data.fields import Field, LabelField, TextField, ListField, MultiLabelField
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer
from allennlp.data.tokenizers import Token, Tokenizer, WhitespaceTokenizer
import numpy as np


@DatasetReader.register('labelledData')
class LabelledData(DatasetReader):
    def __init__(self):
        self.tokenizer = WhitespaceTokenizer()
        self.token_indexers = {'tokens': SingleIdTokenIndexer()}
        self.max_instances: int = None
        self._distributed_info = None
        self._worker_info = None

    @staticmethod
    def clean_train_data(df, name):
        for i in range(len(df)):
            value = re.findall('[^\\(.*][A-Z]{2,}[^(.*\\)]', df[name][i])
            tag = re.findall('\\([A-Z\\d]{4},[A-Z\\d]{4}\\)', df[name][i])
            att = re.findall('(\\s\\b[A-Z]{1}[a-z]*\\b)', df[name][i])
            rep = re.findall(r'ATTRIBUTE*', df[name][i])
            if value:
                for val in value:
                    df.loc[i, name] = df.loc[i, name].replace(val, " VALUE ")
            if tag:
                for t in tag:
                    df.loc[i, name] = df.loc[i, name].replace(t, "TAG")

            if att:
                for a in range(len(att)):
                    if a != 0:
                        df[name][i] = df[name][i].replace(att[a], "")
                    else:
                        df[name][i] = df[name][i].replace(att[a], " ATTRIBUTE ")

        return df

    @staticmethod
    def clean_labels(list_labels):
        labels = []
        for lab in list_labels:
            if lab.__class__ == str:
                labels.append(lab)
        return labels

    def _read(self, file_path: str) -> Iterable[Instance]:
        # with open(file_path, 'r') as lines:
        #     for line in lines:
        #         text, _, _, _, _, _, _= line.strip().split(',')
        #         text_field = TextField(self.tokenizer.tokenize(text),
        #                                self.token_indexers)
        lines = pd.read_csv(file_path)
        cols = lines.columns
        self.clean_train_data(lines, cols[0])
        descriptions = lines[cols[0]]
        labels = list(lines[cols[1:]].iloc[0])
        for line in range(len(lines)):
            text = lines.iloc[line, 0]
            label = list(lines.iloc[line, 1:])
            text_field = TextField(self.tokenizer.tokenize(text),
                                   self.token_indexers)

            fields = {'text': text_field}
            fields['labels'] = MultiLabelField(self.clean_labels(list(lines.iloc[line, 1:])))
            yield Instance(fields)
