import os
import time
import torch
import random
import joblib
import pandas as pd
from abc import ABC
from tqdm import tqdm
from torch_geometric.data import Data
from torch_geometric.data import Batch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

from ._MPG_util import Self_loop, Add_seg_id
from ._Preprocess import NormalizeName, PreEcfp, PreSmiles, PreGraph, ImageDataset
from ._Preprocess import GetCellFeat, GetDrugFeat

_Self_loop = Self_loop()
_Add_seg_id = Add_seg_id()


class DrRead:
    """"""

    @staticmethod
    def PairCSV(csv_path: str):
        assert csv_path[-4:] == '.csv'
        index = [0, 1, 2]
        print('Start reading!')
        csv = pd.read_csv(csv_path, header=0, sep=',', dtype=str)
        Cell = [NormalizeName(each) for each in list(csv.iloc[:, index[0]])]
        Drug = list(csv.iloc[:, index[1]])
        Tag = [float(_) for _ in list(csv.iloc[:, index[2]])]
        pair_ls = [[Cell[i], Drug[i], Tag[i]] for i in range(len(Cell))]
        print('Reading completed!')
        return pair_ls

    @staticmethod
    def PairDef(dataset: str,
                response: str):
        assert dataset in ['CCLE', 'GDSC1', 'GDSC2']
        assert response in ['ActArea', 'AUC', 'IC50']
        pair_ls = dataset + '_' + response
        assert pair_ls in ['CCLE_ActArea', 'CCLE_IC50', 'GDSC1_AUC', 'GDSC1_IC50', 'GDSC2_AUC', 'GDSC2_IC50']
        csv_path = os.path.join(os.path.split(__file__)[0], 'DefaultData/' + pair_ls + '.csv')
        return DrRead.PairCSV(csv_path)

    @staticmethod
    def FeatCell(csv_path: str,
                 subset: bool,
                 subset_path: str = None,
                 save_feat_path: str = None,
                 save_gene_path: str = None):

        return GetCellFeat(csv_path, subset, subset_path, save_feat_path, save_gene_path)

    @staticmethod
    def FeatDrug(csv_path: str,
                 MPG_path: str,
                 save_SMILES_path: str = None,
                 save_MPG_path: str = None):

        return GetDrugFeat(csv_path, MPG_path, save_SMILES_path, save_MPG_path)


class DrData:
    """"""

    def __init__(self, pair_ls: list,
                 cell_ft: str or dict,
                 drug_ft: str or dict,
                 smiles_dict: dict = None,
                 mpg_dict: dict = None):

        if type(cell_ft) == str:
            assert cell_ft in ['EXP', 'PES', 'MUT', 'CNV']
        if type(drug_ft) == str:
            assert drug_ft in ['ECFP', 'SMILES', 'Graph', 'Image']

        self.pair_ls = pair_ls
        self.cell_ft = cell_ft
        self.drug_ft = drug_ft
        self.smiles_dict = smiles_dict
        self.mpg_dict = mpg_dict

    def __len__(self):
        return len(self.pair_ls)

    def clean(self, cell_ft_ls: list = None):
        if cell_ft_ls is None:
            cell_ft_ls = [self.cell_ft] if type(self.cell_ft) == dict else ['GDSC_{}.pkl'.format(self.cell_ft)]
        else:
            cell_ft_ls += [self.cell_ft] if type(self.cell_ft) == dict else ['GDSC_{}.pkl'.format(self.cell_ft)]
        smiles_dict = 'SMILES_dict.pkl' if self.smiles_dict is None else self.smiles_dict
        drug_dict_for_clean = self.drug_ft if type(self.drug_ft) == dict else smiles_dict
        pair_ls = self.pair_ls
        for each in cell_ft_ls:
            pair_ls = _Clean(pair_ls, each, drug_dict_for_clean)
        return DrData(pair_ls, self.cell_ft, self.drug_ft, self.smiles_dict, self.mpg_dict)

    def split(self, mode: str,
              fold: int,
              ratio: list,
              seed: int,
              save: bool = True,
              save_path: str = None):

        return _Split(self, mode, fold, ratio, seed, save, save_path)


def _Clean(pair_ls: list,
           cell_dict: str or dict,
           drug_dict: str or dict):
    """"""

    if type(cell_dict) == str:
        assert cell_dict in ['GDSC_EXP.pkl', 'GDSC_PES.pkl', 'GDSC_MUT.pkl', 'GDSC_CNV.pkl']
        cell_dict = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/' + cell_dict))

    if type(drug_dict) == str:
        drug_dict = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/' + drug_dict))

    print('Number of original pairs: ' + str(len(pair_ls)))
    pair_ls_cleaned = []
    for each in pair_ls:
        if each[0] in cell_dict and each[1] in drug_dict:
            pair_ls_cleaned.append(each)
    print('Number of efficient pairs: ' + str(len(pair_ls_cleaned)))
    return pair_ls_cleaned


def _Split(dr_data: DrData,
           mode: str,
           fold: int,
           ratio: list,
           seed: int,
           save: bool,
           save_path: str):
    """"""

    assert mode in ['common', 'cell_out', 'drug_out', 'strict']
    assert fold >= 1
    assert (sum(ratio) - 1) < 1e-5

    if fold == 1:
        assert len(ratio) == 3
    else:
        assert len(ratio) == 2

    print('Start splitting!')
    pair_ls, cell_ft, drug_ft = dr_data.pair_ls, dr_data.cell_ft, dr_data.drug_ft
    smiles_dict, mpg_dict = dr_data.smiles_dict, dr_data.mpg_dict

    def get_k_folds(ls):
        train = ls[:int(len(ls) * ratio[0])]
        test = ls[int(len(ls) * ratio[0]):]
        train_k_folds = []
        val_k_folds = []
        for i in range(fold):
            train_k = train[:i * len(train) // fold] + train[(i + 1) * len(train) // fold:]
            val_k = train[i * len(train) // fold: (i + 1) * len(train) // fold]
            train_k_folds.append(train_k)
            val_k_folds.append(val_k)
        return train_k_folds, val_k_folds, test

    def get_pair(ls, index):
        pair = []
        for _each in pair_ls:
            if _each[index] in ls:
                pair.append(_each)
        return pair

    if mode == 'common':
        random.seed(seed)
        random.shuffle(pair_ls)
        if fold == 1:
            train_pair_ls = pair_ls[:int(len(pair_ls) * ratio[0])]
            val_pair_ls = pair_ls[int(len(pair_ls) * ratio[0]): int(len(pair_ls) * (ratio[0] + ratio[1]))]
            test_pair = pair_ls[int(len(pair_ls) * (ratio[0] + ratio[1])):]
        else:
            train_pair_ls, val_pair_ls, test_pair = get_k_folds(pair_ls)

    elif mode == 'cell_out':
        cell_ls = sorted(list(set([each[0] for each in pair_ls])))
        random.seed(seed)
        random.shuffle(cell_ls)
        if fold == 1:
            train_cell = cell_ls[:int(len(cell_ls) * ratio[0])]
            val_cell = cell_ls[int(len(cell_ls) * ratio[0]): int(len(cell_ls) * (ratio[0] + ratio[1]))]
            train_pair_ls = []
            val_pair_ls = []
            test_pair = []
            for each in pair_ls:
                if each[0] in train_cell:
                    train_pair_ls.append(each)
                elif each[0] in val_cell:
                    val_pair_ls.append(each)
                else:
                    test_pair.append(each)
        else:
            train_cell_ls, val_cell_ls, test_cell = get_k_folds(cell_ls)
            train_pair_ls = [get_pair(each, 0) for each in train_cell_ls]
            val_pair_ls = [get_pair(each, 0) for each in val_cell_ls]
            test_pair = get_pair(test_cell, 0)

    elif mode == 'drug_out':
        drug_ls = sorted(list(set([each[1] for each in pair_ls])))
        random.seed(seed)
        random.shuffle(drug_ls)
        if fold == 1:
            train_drug = drug_ls[:int(len(drug_ls) * ratio[0])]
            val_drug = drug_ls[int(len(drug_ls) * ratio[0]): int(len(drug_ls) * (ratio[0] + ratio[1]))]
            train_pair_ls = []
            val_pair_ls = []
            test_pair = []
            for each in pair_ls:
                if each[1] in train_drug:
                    train_pair_ls.append(each)
                elif each[1] in val_drug:
                    val_pair_ls.append(each)
                else:
                    test_pair.append(each)
        else:
            train_drug_ls, val_drug_ls, test_drug = get_k_folds(drug_ls)
            train_pair_ls = [get_pair(each, 1) for each in train_drug_ls]
            val_pair_ls = [get_pair(each, 1) for each in val_drug_ls]
            test_pair = get_pair(test_drug, 1)

    else:
        if fold == 1:
            cell_ls = sorted(list(set([each[0] for each in pair_ls])))
            drug_ls = sorted(list(set([each[1] for each in pair_ls])))
            random.seed(seed)
            random.shuffle(cell_ls)
            random.shuffle(drug_ls)
            ratio = [each ** 0.5 for each in ratio]
            ratio = [each / sum(ratio) for each in ratio]
            train_cell = cell_ls[:int(len(cell_ls) * ratio[0])]
            val_cell = cell_ls[int(len(cell_ls) * ratio[0]): int(len(cell_ls) * (ratio[0] + ratio[1]))]
            train_drug = drug_ls[:int(len(drug_ls) * ratio[0])]
            val_drug = drug_ls[int(len(drug_ls) * ratio[0]): int(len(drug_ls) * (ratio[0] + ratio[1]))]
            train_pair_ls = []
            val_pair_ls = []
            test_pair = []
            for each in pair_ls:
                if each[0] in train_cell and each[1] in train_drug:
                    train_pair_ls.append(each)
                elif each[0] in val_cell and each[1] in val_drug:
                    val_pair_ls.append(each)
                elif each[0] not in train_cell + val_cell and each[1] not in train_drug + val_drug:
                    test_pair.append(each)
        else:
            print('Strict split k-fold cross-validation is not recommended, set fold=1 or use other splitting modes.')
            return None, None, None

    if fold == 1:
        train_pair_ls = [train_pair_ls]
        val_pair_ls = [val_pair_ls]

    train_dr_data_ls = [DrData(train_pair, cell_ft, drug_ft, smiles_dict, mpg_dict) for train_pair in train_pair_ls]
    val_dr_data_ls = [DrData(val_pair, cell_ft, drug_ft, smiles_dict, mpg_dict) for val_pair in val_pair_ls]
    test_dr_data = DrData(test_pair, cell_ft, drug_ft, smiles_dict, mpg_dict)

    if save:
        if save_path is None:
            t = time.localtime()
            save_path = 'SplitDrData_{}-{}-{}_{}-{}-{}.pkl'.format(t.tm_mon, t.tm_mday, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec)
        assert save_path[-4:] == '.pkl'
        joblib.dump((train_dr_data_ls, val_dr_data_ls, test_dr_data), save_path)
    print('Splitting completed!')
    return train_dr_data_ls, val_dr_data_ls, test_dr_data


class DrDataset(Dataset, ABC):
    """"""

    def __init__(self, dr_data: DrData,
                 radius: int = 2,
                 nBits: int = 512,
                 max_len: int = 230,
                 char_dict: dict = None,
                 right: bool = True,
                 mpg: bool = True):

        super().__init__()
        self._pair_ls = dr_data.pair_ls
        self._cell_ft = dr_data.cell_ft
        self._drug_ft = dr_data.drug_ft
        self._radius = radius
        self._nBits = nBits
        self._max_len = max_len
        self._char_dict = char_dict
        self._right = right
        self._SMILES_dict = dr_data.smiles_dict
        self._MPG_dict = dr_data.mpg_dict
        self._MPG = mpg
        self._data = DrDataset.preprocess(self)

    def __getitem__(self, idx):
        data = self._data[idx]
        return data

    def __len__(self):
        return len(self._data)

    def preprocess(self):

        if type(self._cell_ft) == str:
            assert self._cell_ft in ['EXP', 'PES', 'MUT', 'CNV']
            cell_dict = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/GDSC_{}.pkl'.format(self._cell_ft)))
        else:
            cell_dict = self._cell_ft

        if type(self._drug_ft) == str:
            assert self._drug_ft in ['ECFP', 'SMILES', 'Graph', 'Image']
            if self._SMILES_dict is None:
                drug_dict = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/SMILES_dict.pkl'))
            else:
                drug_dict = self._SMILES_dict
        else:
            drug_dict = self._drug_ft

        if self._MPG_dict is None:
            self._MPG_dict = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/MPG_dict.pkl'))

        data = []
        for i in tqdm(range(len(self._pair_ls))):
            each_pair = self._pair_ls[i]
            if type(cell_dict[each_pair[0]]) == torch.Tensor:
                cell_ft = cell_dict[each_pair[0]]
            else:
                cell_ft = torch.tensor(cell_dict[each_pair[0]], dtype=torch.float32)
            cell_ft = (cell_ft - cell_ft.mean()) / cell_ft.std(dim=0)

            if self._drug_ft == 'ECFP':
                drug_ft = PreEcfp(drug_dict[each_pair[1]], self._radius, self._nBits)
            elif self._drug_ft == 'SMILES':
                drug_ft = PreSmiles(drug_dict[each_pair[1]], self._max_len, self._char_dict, self._right)
            elif self._drug_ft == 'Graph':
                drug_ft = PreGraph(drug_dict[each_pair[1]])
                if self._MPG:
                    try:
                        drug_ft = _Add_seg_id(_Self_loop(Data(x=drug_ft.x, edge_index=drug_ft.edge_index,
                                                              edge_attr=drug_ft.edge_attr,
                                                              mpg_ft=self._MPG_dict[each_pair[1]])))
                    except KeyError:
                        print('MPG feature missing! Set MPG=False or run Data.DrRead.FeatDrug')
            elif self._drug_ft == 'Image':
                drug_ft = ImageDataset([drug_dict[each_pair[1]]])[0]
            else:
                if type(drug_dict[each_pair[1]]) == torch.Tensor:
                    drug_ft = drug_dict[each_pair[1]]
                else:
                    drug_ft = torch.tensor(drug_dict[each_pair[1]], dtype=torch.float32)

            data.append(Data(cell_ft=cell_ft, drug_ft=drug_ft,
                             response=torch.tensor([each_pair[2]], dtype=torch.float32),
                             cell_name=each_pair[0], drug_name=each_pair[1]))
        return data


class DrCollate:
    """"""

    def __init__(self, follow_batch=None,
                 exclude_keys=None):
        self.follow_batch = follow_batch
        self.exclude_keys = exclude_keys

    def __call__(self, batch):
        cell_ft = torch.stack([g.cell_ft for g in batch])
        if type(batch[0].drug_ft) == torch.Tensor:
            drug_ft = torch.stack([g.drug_ft for g in batch])
        else:
            drug_ft = Batch.from_data_list([g.drug_ft for g in batch], self.follow_batch, self.exclude_keys)
        response = torch.stack([g.response for g in batch])
        return cell_ft, drug_ft, response, [g.cell_name for g in batch], [g.drug_name for g in batch]


def DrDataLoader(dataset: DrDataset,
                 batch_size: int,
                 shuffle: bool,
                 follow_batch=None,
                 exclude_keys=None):
    """"""
    collate = DrCollate(follow_batch, exclude_keys)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, collate_fn=collate)
    return dataloader
