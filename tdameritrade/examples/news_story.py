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

import tdameritrade.td.tdstream as tds
import json

def main():
    tdstream = tds.TDStream()
    story_id = 'SN20180503018141'
    data = tdstream.news_story(['EUR/USD','TSLA','AAPL'], fields="0,1,2,3,4,5,6,7,8,9,10")
    print(json.dumps(data, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
    