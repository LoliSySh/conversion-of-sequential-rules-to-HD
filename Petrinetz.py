import os
import pm4py
from pm4py.algo.discovery.inductive import factory as inductive_miner

if __name__ == "__main__":
    #log_path = os.path.join("tests", "compressed_input_data", "08_receipt.xes.gz")
    #log = pm4py.read_xes(log_path)
    #log = pm4py.read_xes(os.path.join("tests","compressed_input_data",r"C:\Users\Loli\BA\output.txt\BA\Datensätze\PermitLog.xes"))
    log = pm4py.read_xes(os.path.join("tests","compressed_input_data",r"C:\Users\Loli\BA\output.txt\BA\Datensätze\BPI_Challenge_2019.xes"))

    #heu_net = pm4py.discover_heuristics_net(log, dependency_threshold=0.99)
   # pm4py.view_heuristics_net(heu_net)
   
    #inductive miner 
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)

    #for heuristic miner 
    #net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log, dependency_threshold=0.60)
   
    #for alpha miner
    #net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)


    
    
    pm4py.view_petri_net(net, initial_marking, final_marking)
   # pm4py.write_pnml(net, initial_marking, final_marking, "petriPermitLog_depthres99.pnml")
  