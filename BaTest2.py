
import pm4py
import pm4py.objects.log.util.sorting

def convert_to_custom_format(log):
    custom_log = " "
    for trace in log : 
        custom_trace = [] 
        for event in trace :
            event_attributes = pm4py.get_event_attributes(log)
            attribute_value_pairs = [(k, next(iter(pm4py.get_event_attribute_values(log,k))))for k in event_attributes]
            custom_trace.extend(attribute_value_pairs)
            custom_trace.append(-1)
        custom_trace.append(-2)
        custom_trace.append("\n")
    custom_log = "".join(str(custom_trace))
    custom_log.replace(", ", " ")
 
    return custom_log
      


if __name__ == "__main__":
 
    log = pm4py.read_xes(r"C:\Users\Loli\BA\output.txt\BA\Datensätze\BPI_Challenge_2019.xes")

    event_log = pm4py.convert_to_event_log(log)
    event_activities = pm4py.get_event_attribute_values(event_log, "concept:name")
    event_activities_maped= dict(zip(event_activities.keys(),range(1,len(event_activities)+1)))
    print(event_activities_maped)

    custom_log=[]
    
    for trace in event_log:
        all_event= [event for event in trace ]
        custom_trace=[]
        all_event.sort(key=lambda x: x['time:timestamp'])
        
        for event in all_event:            
            x = event["concept:name"]
            y = event_activities_maped[x]
            custom_trace.extend(str(y) +" " )
            #event_activities_maped = dict(map(lambda num: num,  range(1,len(event_activities)+1) ))
            #custom_trace.extend( map(lambda value: str( trace ) +" " + str (value)+" -1 ", event_activities.keys()))
            custom_trace.append("-1 ")
        custom_trace.append("-2")
        custom_trace.append('\n')
        custom_log.extend(custom_trace)
    x = "".join(map(str, custom_log))
    print(x)

               
    with open("ergebnis - Kopie.txt", "w") as txt_file:
        txt_file.write(x)
 
            

    
       
    
    
    


    
