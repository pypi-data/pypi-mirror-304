import os
import time
import torch
import joblib
import numpy as np
import pandas as pd
from rdkit import Chem
import pubchempy as pcp
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from torch.utils.data import Dataset
import torchvision.transforms as transforms

from ._MPG_model import MolGNet
from ._MPG_util import Self_loop, Add_seg_id
from ._MPG_loader import mol_to_graph_data_obj_complex

_char_ls = ["7", "6", "o", "]", "3", "s", "(", "-", "S", "/", "B", "4", "[", ")", "#", "I", "l", "O", "H", "c", "t", "1", "@",
            "=", "n", "P", "8", "C", "2", "F", "5", "r", "N", "+", "\\", ".", " "]
_max_len = 230

_Self_loop = Self_loop()
_Add_seg_id = Add_seg_id()


def NormalizeName(string: str):
    """"""
    lt = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    string = string.upper()
    std_string = ''
    for char in string:
        if char in lt:
            std_string += char
    return std_string


def _GetEcfp(smiles: str,
             radius: int,
             nBits: int):
    """"""
    mol = AllChem.MolFromSmiles(smiles)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=nBits)
    ECFP = np.zeros((nBits,), dtype=int)
    on_bits = list(fp.GetOnBits())
    ECFP[on_bits] = 1
    return ECFP.tolist()


def PreEcfp(smiles: str,
            radius: int,
            nBits: int):
    """"""
    smiles = AllChem.MolToSmiles(AllChem.MolFromSmiles(smiles), isomericSmiles=True, canonical=True)
    return torch.tensor(_GetEcfp(smiles, radius, nBits), dtype=torch.float32)


def _PadSmiles(smiles: str,
               max_len: int,
               right: bool):
    """"""
    if max_len is None:
        max_len = _max_len
    assert max_len >= len(smiles)
    if right:
        return smiles + " " * (max_len - len(smiles))
    else:
        return " " * (max_len - len(smiles)) + smiles


def PreSmiles(smiles: str,
              max_len: int,
              char_dict: dict,
              right: bool):
    """"""
    if char_dict is None:
        char_dict = dict(zip(_char_ls, [i for i in range(len(_char_ls))]))
    smiles = _PadSmiles(AllChem.MolToSmiles(AllChem.MolFromSmiles(smiles), isomericSmiles=True, canonical=True), max_len, right)
    return torch.tensor([char_dict[c] for c in smiles], dtype=torch.int)


def PreGraph(smiles: str):
    """"""
    smiles = AllChem.MolToSmiles(AllChem.MolFromSmiles(smiles), isomericSmiles=True, canonical=True)
    return _Add_seg_id(_Self_loop(mol_to_graph_data_obj_complex(AllChem.MolFromSmiles(smiles))))


class ImageDataset(Dataset):
    def __init__(self, smiles_ls):
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                              std=[0.229, 0.224, 0.225])
        self.transform = transforms.Compose([transforms.CenterCrop(224),
                                             transforms.ToTensor()])
        self.img_ls, self.smiles_err = self.smiles2img(smiles_ls)

    def __getitem__(self, index):
        return self.img_ls[index]

    def __len__(self):
        return len(self.img_ls)

    def smiles2img(self, smiles_ls):
        img_ls = []
        smiles_err = []
        for smiles in smiles_ls:
            try:
                mol = Chem.MolFromSmiles(smiles)
                img = Draw.MolsToGridImage([mol], molsPerRow=1, subImgSize=(224, 224))
                img_ls.append(self.normalize(self.transform(img.convert('RGB'))))
            except:
                smiles_err.append(smiles)
        if len(smiles_err) != 0:
            print("smiles error: {}".format(len(smiles_err)))
        return img_ls, smiles_err


def GetCellFeat(csv_path: str,
                subset: bool,
                subset_path: str,
                save_feat_path: str,
                save_gene_path: str):
    """"""

    assert csv_path[-4:] == '.csv'
    dataset = pd.read_csv(csv_path, header=None, sep=',', low_memory=False)
    cells = [NormalizeName(str(_)) for _ in list(dataset.iloc[0, 1:])]
    genes = [NormalizeName(str(_)) for _ in list(dataset.iloc[1:, 0])]
    data = np.array(dataset.iloc[1:, 1:], dtype=float)
    mean_value = np.nanmean(data)
    data = np.where(np.isnan(data), mean_value, data)

    if not subset:
        GeneList = genes
    else:
        if subset_path is None:
            subset_path = os.path.join(os.path.split(__file__)[0], 'DefaultData/key.genes.txt')
        assert subset_path[-4:] == '.txt'
        f = open(subset_path, encoding='gbk')
        GeneList = []
        for each_row in f:
            GeneList.append(NormalizeName(each_row.strip()))

        GeneIdx = []
        for each in GeneList:
            try:
                GeneIdx.append(genes.index(each))
            except ValueError:
                GeneIdx.append(-1)

        data = np.append(data, np.ones((1, len(cells))) * mean_value, axis=0)
        data = data[GeneIdx, :]

    CellFeat = dict()
    for i in range(len(cells)):
        feat = data[:, i]
        CellFeat[cells[i]] = ((feat - feat.mean()) / feat.std()).tolist()

    t = time.localtime()
    if save_feat_path is None:
        save_feat_path = 'CellFeat_{}-{}-{}_{}-{}-{}.pkl'.format(t.tm_mon, t.tm_mday, t.tm_year,
                                                                 t.tm_hour, t.tm_min, t.tm_sec)
    if save_gene_path is None:
        save_gene_path = 'GeneList_{}-{}-{}_{}-{}-{}.pkl'.format(t.tm_mon, t.tm_mday, t.tm_year,
                                                                 t.tm_hour, t.tm_min, t.tm_sec)

    assert save_feat_path[-4:] == '.pkl'
    assert save_gene_path[-4:] == '.pkl'
    joblib.dump(CellFeat, save_feat_path)
    joblib.dump(GeneList, save_gene_path)

    return CellFeat, GeneList


def _GetSMILESDict(drugs: list):
    """"""
    print('Retrieving SMILES strings...')
    SMILES_dict_def = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/SMILES_dict.pkl'))
    SMILES_dict = dict()
    SMILES_not_found = []
    for each in drugs:
        if each in SMILES_dict_def:
            SMILES_dict[each] = SMILES_dict_def[each]
        else:
            try:
                _ = pcp.get_compounds(each, 'name')
                SMILES_dict[each] = _[0].isomeric_smiles
            except:
                SMILES_not_found.append(each)
    print('Total: {}  Successful: {}'.format(len(drugs), len(drugs) - len(SMILES_not_found)))
    return SMILES_dict


def _GetMPGDict(SMILES_dict: dict,
                MPG_path: str):
    """"""
    MPG_dict = dict()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gnn = MolGNet(num_layer=5, emb_dim=768, heads=12, num_message_passing=3, drop_ratio=0)
    gnn.load_state_dict(torch.load(MPG_path))
    gnn = gnn.to(device)
    gnn.eval()
    with torch.no_grad():
        for each in SMILES_dict:
            graph = PreGraph(SMILES_dict[each]).to(device)
            MPG_dict[each] = gnn(graph).cpu()
    return MPG_dict


def GetDrugFeat(csv_path: str,
                MPG_path: str,
                save_SMILES_path: str,
                save_MPG_path: str):
    """"""

    assert csv_path[-4:] == '.csv'
    csv = pd.read_csv(csv_path, header=0, sep=',', dtype=str)
    drugs = list(csv.iloc[:, 1])

    SMILES_dict = _GetSMILESDict(drugs)

    t = time.localtime()
    if save_SMILES_path is None:
        save_SMILES_path = 'SMILESDict_{}-{}-{}_{}-{}-{}.pkl'.format(t.tm_mon, t.tm_mday, t.tm_year,
                                                                     t.tm_hour, t.tm_min, t.tm_sec)
        joblib.dump(SMILES_dict, save_SMILES_path)

    if MPG_path is None:
        MPG_dict = None
    else:
        assert MPG_path[-3:] == '.pt'
        MPG_dict = _GetMPGDict(SMILES_dict, MPG_path)
        if save_MPG_path is None:
            save_MPG_path = 'MPGDict_{}-{}-{}_{}-{}-{}.pkl'.format(t.tm_mon, t.tm_mday, t.tm_year,
                                                                   t.tm_hour, t.tm_min, t.tm_sec)
        joblib.dump(MPG_dict, save_MPG_path)

    return SMILES_dict, MPG_dict
