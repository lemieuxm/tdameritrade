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

import datetime as dt
import tdameritrade.td.tdstream as tds
import time

def chartHistory():
    tdstream = tds.TDStream()
    from tdameritrade import UTC
    startTime = dt.datetime(2017, 2, 1, 0, 0, 0, tzinfo=UTC)
    endTime = dt.datetime(2017, 3, 1, 0, 0, 0, tzinfo=UTC)
    # m1, m5, m10, m30, h1, d1, w1, n1
    tdstream.chartHistory("EUR/USD", "h1", startTime, endTime, chartHistoryHandler)
    print("finished")
    wait()    
    
def chartHistoryHandler(data):
    from tdameritrade import UTC
    snapshot = data['snapshot']
    content = snapshot[0]['content']
    samples = content[0]['3']
    numSamples = content[0]['2']  # @UnusedVariable
    key = content[0]['key']  # @UnusedVariable
    sampleTimes = []
    for sample in samples:
        t = sample['0']
        sampleTimes.append(int(t/1000.0))
        dtime = dt.datetime.fromtimestamp(int(t/1000.0), UTC)  # @UnusedVariable
        periodOpen = sample['1']  # @UnusedVariable
        high = sample['2']  # @UnusedVariable
        #print(dtime.strftime("%Y-%m-%d %H:%M") +" --> high:"+ str(high))
        low = sample['3']  # @UnusedVariable
        close = sample['4']  # @UnusedVariable
        volume = sample['5']  # @UnusedVariable
    sampleTimes.sort()
    print("min: "+str(dt.datetime.fromtimestamp(min(sampleTimes), UTC)))
    print("max: "+str(dt.datetime.fromtimestamp(max(sampleTimes), UTC)))
    lastSampleTime = min(sampleTimes)  # @UnusedVariable
    for sampleTime in sampleTimes:
        delta = sampleTime - lastSampleTime
        print(str(sampleTime) +" - " + str(dt.datetime.fromtimestamp(sampleTime, UTC)) + ": "+str(delta))
        lastSampleTime = sampleTime
    pass

i = 10
def wait(m=10):
    global i
    while i < m:
        time.sleep(1)
        # doing nothing but keeping the thread going


if __name__ == '__main__':
    chartHistory()
    