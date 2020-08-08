# -*- coding:utf-8 -*-
from factor.base_factor import BaseFactor
from data.data_module import DataModule

class PEFactor(BaseFactor):
    def __init__(self):
        BaseFactor.__init__(self,'pe')

    def compute(self,begin_date=None,end_date=None):
        print(self.name,flush=True)

        dm = DataModule()

        df_daily = dm.pro_bar()
        print(df_daily)


if __name__ == '__main__':
    PEFactor().compute()