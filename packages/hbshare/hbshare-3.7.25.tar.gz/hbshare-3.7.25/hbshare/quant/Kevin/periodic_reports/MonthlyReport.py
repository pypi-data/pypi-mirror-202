"""
Alpha月报
"""
import os
import numpy as np
import pandas as pd
import hbshare as hbs
import datetime
import math
from sqlalchemy import create_engine
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_fund_nav_from_sql, get_trading_day_list


class MonthlyReporter:
    def __init__(self, trade_date):
        self.trade_date = trade_date
        self._date_preprocess()

    def _date_preprocess(self):
        pass



if __name__ == '__main__':
    MonthlyReporter(trade_date="20230331")