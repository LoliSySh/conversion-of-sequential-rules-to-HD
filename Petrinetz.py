import os
import pm4py
from pm4py.algo.discovery.inductive import factory as inductive_miner

if __name__ == "__main__":

    log = pm4py.read_xes(os.path.join("tests","compressed_input_data",r"PATH TO DATASET\Dataset.xes"))
   
    #inductive miner 
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)

    #for heuristic miner 
    #net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log, dependency_threshold=0.60)
   
    #for alpha miner
    #net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)


    
    
    pm4py.view_petri_net(net, initial_marking, final_marking)
  
