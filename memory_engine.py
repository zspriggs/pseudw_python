from engine import GreekQueryEngine, GreekTextParser, Word
from typing import List

import os
import pandas as pd

class MemoryHelper:

    def __init__(self, URNs: List[Word]):
        self.urns = URNs
        if len(URNs) == 0: #if len is 0, get all urns
            df = pd.read_csv("matched_urns.csv") #fetch document list
            self.urns = df['URN']

        self.doc_count = len(self.urns)

    def query(self, query):
        results = []
        max_docs = 5

        for start_id in range(0, self.doc_count, max_docs):
            urn_batch = self.urns[start_id:start_id+max_docs]
            print(f"using urns: {urn_batch}")

            small_engine = create_engine_from_urns(urn_batch)
            batch_results = small_engine.query(query)
            results.append(batch_results) #If memory issues persist, can change this to write 
            #add gc.collect?

        return results

def create_query_engine(xml_docs: dict[str, str]) -> GreekQueryEngine:
    parser = GreekTextParser()
    all_words = []
    print("loading ", len(xml_docs.items()), " items...")
    for urn, content in xml_docs.items():
        words = parser.xml_to_words(content, urn)
        all_words.extend(words)
    print("successfully loaded items, creating engine")
    return GreekQueryEngine(all_words)


def create_engine_from_urns(urns: List[str]):
    ''' Create query engine from URN list. If list is empty, use all documents.'''

    this_dir = os.path.dirname(__file__)
    all_files = {}

    if len(urns) == 0:
        df = pd.read_csv("matched_urns.csv") #fetch document list
        urns = df['URN']

    for urn in urns:
        doc_path = os.path.join(this_dir, "data", "xml", f"{urn}.xml")
        try:
            with open(doc_path, 'rb') as doc: 
                xml_content = doc.read().decode('utf-8')
                all_files[urn] = xml_content
        except: 
            print(f"Error opening document with urn {urn}.")    

    print("Opened documents")
    return create_query_engine(all_files)