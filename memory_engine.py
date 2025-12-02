from engine import Word
from engine import get_engine_from_urns
from typing import List

import os
import pandas as pd


class MemoryHelper:
    def __init__(self, URNs: List[Word], batch_size=4):
        self.urns = URNs
        if len(URNs) == 0: #if len is 0, get all urns
            df = pd.read_csv("matched_urns.csv") #fetch document list
            self.urns = df['URN']

        self.doc_count = len(self.urns)
        self.batch_size = batch_size
    
    def query(self, query):
        print("qyuery)")
        results = []
        total_batches = int(self.doc_count/self.batch_size) + 1
        progress = 0

        for start_id in range(0, self.doc_count, self.batch_size):
            print(f"start batch {progress}")
            urn_batch = self.urns[start_id:start_id+self.batch_size]

            small_engine = get_engine_from_urns(urn_batch)
            batch_results = small_engine.query(query)
            print(type(batch_results))

            if len(results) == 0:
                results=batch_results
            else:
                results.extend(batch_results)

            progress += 1
            yield progress/total_batches, batch_results
    

            #results.append(batch_results) #If memory issues persist, can change this to write 

        yield 1, results