

from typing import Tuple, Iterable, Optional, Union, Mapping

import os, random
import numpy as np
import pandas as pd
from math import floor, ceil

from ..tags import USER, ITEM, RATING, TIMESTAMP

from ...utils import infoLogger, mkdirs


__all__ = ['AtomicConverter']


NAME_FORMAT_DICT = {
    'user_id': USER.name,
    'item_id': ITEM.name,
    'venue_id': ITEM.name, # FourSquare
    'rating': RATING.name,
    'timestamp': TIMESTAMP.name
}


TYPE_FORMAT_DICT = {
    'token': str,
    'token_seq': str,
    'float': float,
    # 'float_seq': None
}


class AtomicConverter:
    r"""
    How to convert Atomic files into train|valid|test.txt ?

    Flows:
    ------
    1. Download corresponding files from [[RecBole](https://drive.google.com/drive/folders/1so0lckI6N6_niVEYaBu-LIcpOdZf99kj)].
    2. Import corresponding dataset.
    3. Call `make_xxx_dataset'.

    Parameters:
    -----------
    root: str
        The root of data.
    filename: str
        The file with Atomic files.
        - `None': Use cls.filename instead.
    dataset: str, optional
        The filename saving dataset.
        - `None': Use classname instead.
    """
    filename: str

    _name_format_dict = dict()
    _type_format_dict = dict()

    def __init__(
        self, root: str, 
        filename: Optional[str] = None,
        dataset: Optional[str] = None
    ) -> None:
        super().__init__()

        filename = filename if filename else self.filename
        self.path = os.path.join(root, filename)
        if not os.path.exists(self.path) or not any(True for _ in os.scandir(self.path)):
            raise FileNotFoundError(f"No such file of {self.path}, or this dir is empty ...")

        self.root = root
        self.dataset = dataset if dataset else self.__class__.__name__

        self._name_format_dict.update(NAME_FORMAT_DICT)
        self._type_format_dict.update(TYPE_FORMAT_DICT)

    def convert_by_column(self, df: pd.DataFrame):
        old_columns = df.columns
        new_columns = []

        for col in old_columns:
            col = col.lower()
            name_, type_ = col.split(":")
            name_ =  self._name_format_dict.get(name_, name_.capitalize())
            type_ = self._type_format_dict[type_]
            df[col] = df[col].astype(type_)

            new_columns.append(name_)
        
        df.columns = new_columns
        return df

    def load_inter_file(self):
        for file_ in os.scandir(self.path):
            filename = file_.name
            if not filename.endswith('.inter'):
                continue
            file_ = os.path.join(self.path, filename)
            df = pd.read_csv(file_, delimiter='\t')
            infoLogger(f"[Converter] >>> Load `{filename}' ...")
            return self.convert_by_column(df)
        infoLogger(f"[Converter] >>> No file ends with `.inter' ...")

    def load_user_file(self):
        for file_ in os.scandir(self.path):
            filename = file_.name
            if not filename.endswith('.user'):
                continue
            file_ = os.path.join(self.path, filename)
            df = pd.read_csv(file_, delimiter='\t')
            infoLogger(f"[Converter] >>> Load `{filename}' ...")
            return self.convert_by_column(df)
        infoLogger(f"[Converter] >>> No file ends with `.user' ...")

    def load_item_file(self):
        for file_ in os.scandir(self.path):
            filename = file_.name
            if not filename.endswith('.item'):
                continue
            file_ = os.path.join(self.path, filename)
            df = pd.read_csv(file_, delimiter='\t')
            infoLogger(f"[Converter] >>> Load `{filename}' ...")
            return self.convert_by_column(df)
        infoLogger(f"[Converter] >>> No file ends with `.user' ...")

    def load_kg_file(self):
        raise NotImplementedError()

    def load_link_file(self):
        raise NotImplementedError()

    def load_net_file(self):
        raise NotImplementedError()

    def load(self):
        self.interactions = self.load_inter_file()
        self.userFeats = self.load_user_file()
        self.itemFeats = self.load_item_file()
        self.pools = (self.interactions, self.userFeats, self.itemFeats)

    def reserve(self, columns: Iterable[str]):
        all_columns = self.interactions.columns
        columns_ = set(columns) & set(all_columns)
        columns = sorted(columns_, key=columns.index)
        infoLogger(f"[Converter] >>> Reserve fields: {columns} ...")
        self.interactions = self.interactions[columns]

    def exclude(self, columns: Iterable[str]):
        all_columns = self.interactions.columns
        columns = set(all_columns) - set(columns)
        columns = sorted(columns, key=all_columns.index)
        infoLogger(f"[Converter] >>> Exclude fields: {columns} ...")
        self.interactions = self.interactions[columns]

    def reorder(self, columns: Iterable[str] = (USER.name, ITEM.name)):
        all_columns = self.interactions.columns
        columns = columns + all_columns
        columns_ = set(columns) & set(all_columns)
        columns = sorted(columns_, key=columns.index)
        infoLogger(f"[Converter] >>> Reorder fields: {columns} ...")
        self.interactions = self.interactions[columns]

    def map_col(
        self, col: str, mapper: Mapping, 
        pools: Optional[Iterable[pd.DataFrame]] = None
    ):
        pools = self.pools if pools is None else pools
        for df in pools:
            if df is not None:
                df[col] = df[col].map(mapper)

    def filter_by_rating(
        self, 
        low: Union[None, int, float] = None, 
        high: Union[None, int, float] = None
    ):
        try:
            df = self.interactions
            ratings = df[RATING.name]
            low = low if low is not None else ratings.min()
            high = high if high is not None else ratings.max()
            self.interactions = df[(low <= ratings) & (ratings <= high)]
            infoLogger(f"[Converter] >>> Filter dataframe according to {RATING.name} ...")
        except KeyError:
            infoLogger(
                f"[Converter] >>> Skip `filter_by_rating` because of `inter` has no field of `{RATING.name}' ..."
            )
    
    def filter_by_core(
        self,
        low4user: Union[None, int, float] = None, 
        high4user: Union[None, int, float] = None,
        low4item: Union[None, int, float] = None, 
        high4item: Union[None, int, float] = None
    ):
        r"""
        Filter (user, item) by k-core settings.

        Parameters:
        -----------
        low4user: int, float, optional
            Minimum core for user.
            - `None`: float('-inf')
        max4user: int, float, optional
            Maximum core for user.
            - `None`: float('inf')
        low4item: int, float, optional
            Minimum core for item.
            - `None`: float('-inf')
        max4item: int, float, optional
            Maximum core for item.
            - `None`: float('inf')
        """
        low4user = low4user if low4user else float('-inf')
        high4user = high4user if high4user else float('inf')
        low4item = low4item if low4item else float('-inf')
        high4item = high4item if high4item else float('inf')
        df = self.interactions
        dsz = -1
        infoLogger(
            f"[Converter] >>> Filter dataframe: "
            f"User in [{low4user}, {high4user}]; "
            f"Item in [{low4item}, {high4item}] ..."
        )
        infoLogger(f"[Converter] >>> Current datasize: {len(df)} ...")
        while dsz != len(df):
            # filter by user
            dsz = len(df)
            users = df[USER.name]
            counts = users.value_counts()
            bool_indices = users.isin(
                counts[(low4user <= counts) & (counts <= high4user)].index
            )
            df = df[bool_indices]

            # filter by item
            items = df[ITEM.name]
            counts = items.value_counts()
            bool_indices = items.isin(
                counts[(low4item <= counts) & (counts <= high4item)].index
            )
            df = df[bool_indices]

            infoLogger(f"[Converter] >>> Current datasize: {len(df)}")

        self.interactions = df

    def user2token(self):
        infoLogger(f"[Converter] >>> Map user ID to Token ...")
        user_ids = sorted(self.interactions[USER.name].unique().tolist())
        self.userCount = len(user_ids)

        user_tokens = list(range(len(user_ids)))
        self.userMaps = dict(
            zip(user_ids, user_tokens)
        )

        if self.userFeats is not None:
            self.userFeats = self.userFeats[self.userFeats[USER.name].isin(user_ids)]
            self.userFeats = self.userFeats.sort_values([USER.name])

        self.map_col(
            USER.name, self.userMaps, 
            pools=(self.interactions, self.userFeats)
        )

    def item2token(self):
        infoLogger(f"[Converter] >>> Map item ID to Token ...")
        item_ids = sorted(self.interactions[ITEM.name].unique().tolist())
        self.itemCount = len(item_ids)

        item_tokens = range(len(item_ids))
        self.itemMaps = dict(
            zip(item_ids, item_tokens)
        )

        if self.itemFeats is not None:
            self.itemFeats = self.itemFeats[self.itemFeats[ITEM.name].isin(item_ids)]
            self.itemFeats = self.itemFeats.sort_values([ITEM.name])

        self.map_col(
            ITEM.name, self.itemMaps, 
            pools=(self.interactions, self.itemFeats)
        )

    def sort_by_timestamp(self):
        df = self.interactions
        try:
            df = df.sort_values(by=[USER.name, TIMESTAMP.name])
            infoLogger(f"[Converter] >>> Sort by [{USER.name}] [{TIMESTAMP.name}] ...")
        except KeyError:
            df = df.sort_values(by=[USER.name])
            infoLogger(f"[Converter] >>> Sort by [{USER.name}] ...")
        finally:
            self.interactions = df

    def gen_split_by_ratio(self, ratios: Iterable = (8, 1, 1)):
        infoLogger(f"[Converter] >>> Split by ratios: {ratios} ...")
        traingroups = []
        validgroups = []
        testgroups = []
        markers = np.cumsum(ratios)
        for _, group in self.interactions.groupby(USER.name):
            if len(group) == 0:
                continue
            l = max(floor(markers[0] * len(group) / markers[-1]), 1)
            r = floor(markers[1] * len(group) / markers[-1])
            traingroups.append(group[:l])
            if l < r:
                validgroups.append(group[l:r])
            if r < len(group):
                testgroups.append(group[r:])

        self.trainiter = pd.concat(traingroups).reset_index(drop=True)
        self.validiter = pd.concat(validgroups).reset_index(drop=True)
        self.testiter = pd.concat(testgroups).reset_index(drop=True)

    def seq_split_by_ratio(self, ratios: Iterable = (8, 1, 1), seed: int = 0):
        infoLogger(f"[Converter] >>> Split by ratios: {ratios} ...")
        markers = np.cumsum(ratios)
        groups = [pair[1] for pair in self.interactions.groupby(USER.name)]

        l = max(floor(markers[0] * len(groups) / markers[-1]), 1)
        r = floor(markers[1] * len(groups) / markers[-1])

        random.seed(seed)
        random.shuffle(groups)

        traingroups = groups[:l]
        validgroups = groups[l:r]
        testgroups = groups[r:]

        self.trainiter = pd.concat(traingroups).reset_index(drop=True)
        self.validiter = pd.concat(validgroups).reset_index(drop=True)
        self.testiter = pd.concat(testgroups).reset_index(drop=True)

    def seq_split_by_last_two(self):
        infoLogger(f"[Converter] >>> Split by leaving last two ...")
        traingroups = []
        validgroups = []
        testgroups = []
        for _, group in self.interactions.groupby(USER.name):
            if len(group) == 0:
                continue
            if len(group) <= 3:
                traingroups.append(group)
            else:
                traingroups.append(group[:-2])
                validgroups.append(group[-2:-1])
                testgroups.append(group[-1:])

        self.trainiter = pd.concat(traingroups).reset_index(drop=True)
        self.validiter = pd.concat(validgroups).reset_index(drop=True)
        self.testiter = pd.concat(testgroups).reset_index(drop=True)

    def save(self, path: str):
        mkdirs(path)

        infoLogger(f"[Converter] >>> Save `train.txt' to {path} ...")
        df = pd.DataFrame(self.trainiter)
        df.to_csv(os.path.join(path, 'train.txt'), sep='\t', index=False)

        infoLogger(f"[Converter] >>> Save `valid.txt' to {path} ...")
        df = pd.DataFrame(self.validiter)
        df.to_csv(os.path.join(path, 'valid.txt'), sep='\t', index=False)

        infoLogger(f"[Converter] >>> Save `test.txt' to {path} ...")
        df = pd.DataFrame(self.testiter)
        df.to_csv(os.path.join(path, 'test.txt'), sep='\t', index=False)

        if self.userFeats is not None:
            infoLogger(f"[Converter] >>> Save `user.txt' to {path} ...")
            self.userFeats.to_csv(
                os.path.join(path, 'user.txt'),
                sep='\t', index=False
            )

        if self.itemFeats is not None:
            infoLogger(f"[Converter] >>> Save `item.txt' to {path} ...")
            self.itemFeats.to_csv(
                os.path.join(path, 'item.txt'),
                sep='\t', index=False
            )

        self.summary()

    def make_general_dataset(
        self,
        star4pos: int = 0,
        kcore4user: int = 10,
        kcore4item: int = 10,
        ratios: Tuple[int, int, int] = (8, 1, 1),
        fields: Iterable[str] = (USER.name, ITEM.name)
    ):
        r"""
        Make general dataset.

        Parameters:
        -----------
        star4pos: int, default to 0
            Select interactions with `Rating > star4pos'.
        kcore4user: int, default to 10
            Select kcore interactions according to User.
        kcore4item: int, default to 10
            Select kcore interactions according to Item.
        ratios: Tuple[int, int, int], default to (8, 1, 1)
            The ratios of training|validation|test set.
        fields: Iterable[str], default to (User, Item)
            The fields reserved.
        """

        self.load()
        self.filter_by_rating(low=star4pos, high=None)
        self.filter_by_core(low4user=kcore4user, low4item=kcore4item)
        self.user2token()
        self.item2token()
        self.sort_by_timestamp()
        self.reserve(fields)
        self.gen_split_by_ratio(ratios)

        code = f"{kcore4user}{kcore4item}{star4pos}{''.join(map(str, ratios))}"
        path = os.path.join(
            self.root, 'General', 
            '_'.join([self.dataset, code, 'Chron'])
        )

        self.save(path)

    def make_sequential_dataset(
        self,
        star4pos: int = 0,
        kcore4user: int = 5,
        kcore4item: int = 5,
        fields: Iterable[str] = (USER.name, ITEM.name)
    ):
        r"""
        Make sequential dataset by leaving last two as validation|test samples.

        Parameters:
        -----------
        star4pos: int, default to 0
            Select interactions with `Rating > star4pos'.
        kcore4user: int, default to 10
            Select kcore interactions according to User.
        kcore4item: int, default to 10
            Select kcore interactions according to Item.
        fields: Iterable[str], default to (User, Item)
            The fields reserved.
        """


        self.load()
        self.filter_by_rating(low=star4pos, high=None)
        self.filter_by_core(low4user=kcore4user, low4item=kcore4item)
        self.user2token()
        self.item2token()
        self.sort_by_timestamp()
        self.reserve(fields)
        self.seq_split_by_last_two()

        code = f"{kcore4user}{kcore4item}{star4pos}"
        path = os.path.join(
            self.root, 'Sequential', 
            '_'.join([self.dataset, code, 'Chron'])
        )

        self.save(path)

    def make_sequential_dataset_by_ratio(
        self,
        star4pos: int = 0,
        kcore4user: int = 5,
        kcore4item: int = 5,
        ratios: Tuple[int, int, int] = (8, 1, 1),
        fields: Iterable[str] = (USER.name, ITEM.name),
        seed: int = 0
    ):
        r"""
        Make sequential dataset by ratios.

        Parameters:
        -----------
        star4pos: int, default to 0
            Select interactions with `Rating > star4pos'.
        kcore4user: int, default to 10
            Select kcore interactions according to User.
        kcore4item: int, default to 10
            Select kcore interactions according to Item.
        ratios: Tuple[int, int, int], default to (8, 1, 1)
            The ratios of training|validation|test set.
        fields: Iterable[str], default to (User, Item)
            The fields reserved.
        """
        self.load()
        self.filter_by_rating(low=star4pos, high=None)
        self.filter_by_core(low4user=kcore4user, low4item=kcore4item)
        self.user2token()
        self.item2token()
        self.sort_by_timestamp()
        self.reserve(fields)
        self.seq_split_by_ratio(ratios, seed=seed)

        code = f"{kcore4user}{kcore4item}{star4pos}{''.join(map(str, ratios))}"
        path = os.path.join(
            self.root, 'Sequential', 
            '_'.join([self.dataset, code, 'Chron'])
        )

        self.save(path)

    def summary(self):
        from prettytable import PrettyTable
        table = PrettyTable(['#User', '#Item', '#Interactions', '#Train', '#Valid', '#Test', 'Density'])
        trainsize = len(self.trainiter)
        validsize = len(self.validiter)
        testsize = len(self.testiter)
        table.add_row([
            self.userCount, self.itemCount, trainsize + validsize + testsize,
            trainsize, validsize, testsize,
            (trainsize + validsize + testsize) / (self.userCount * self.itemCount)
        ])
        infoLogger(table)