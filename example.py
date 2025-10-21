from memory_engine import MemoryHelper
import pickle

mem_engine = MemoryHelper([])
results = mem_engine.query("εἰ ~ ἀγαθός:comparative & εἰ ~ εἰμί")

print(len(results))
with open('data.pkl', 'wb') as file:
    pickle.dump(results, file)