"""
    Copyright (C) 2018 Matthew LeMieux
    
    This file is part of a third party TDAmeritrade API Library, called MLTDAmeritrade.

    MLTDAmeritrade is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MLTDAmeritrade is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MLTDAmeritrade.  If not, see <http://www.gnu.org/licenses/>.
"""


import json
import tdameritrade.td.tddata as tdd
import datetime as dt
from tdameritrade import UTC  

def nminbyday(symbol):
    tdData = tdd.TdData()
    startDate = dt.datetime(2018, 4, 1, tzinfo=UTC)
    endDate = startDate + dt.timedelta(days=10)
    data = tdData.getNMinByDay(symbol, startDate, endDate, 5)
    print(json.dumps(data, indent=4, sort_keys=True))
    print("finished running nminbyday") 

if __name__ == '__main__':
    nminbyday("AAPL")
    