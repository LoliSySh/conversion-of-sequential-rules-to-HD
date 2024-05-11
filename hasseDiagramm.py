import graphviz as grv


def extract_data(log, name):
    relation = []
    graphDic = {}
    for line in log:
        parts = line.split('==>')        
        antecedent = {int(value) for value in parts[0].split(',')} if ',' in parts[0].strip() else {int(parts[0].strip())}
        t = parts[1].split('#SUP:')[0].strip()
        consequent = {int(value) for value in t.split(',')} if ',' in t else {int(t)}
        #{('1 ', ' 2,3 '): (4, 1.0)}    
        
             
        sup_value = float(parts[1].split('#SUP:')[1].split('#CONF:')[0].strip())
        conf_value = float(parts[1].split('#CONF:')[1].strip())

        
        # edge ist eine Liste aus tupeln die aus int sets bestehen (antecedent, (antecedent.union(consequent)))
        #{({1}, {2,3})} 
        edge = [(antecedent, (antecedent.union(consequent)))]

        graphDic.update({str(edge[0]): (sup_value, conf_value) })
        relation.extend(edge)
        print(relation)
 
    same_antecedent = []
    same_consequent = []
    rest =[]
    
   
    all_targs= [tupel[1] for tupel in relation ]
    transitiv_rel = is_transitiv(relation,all_targs)
    
    for rel in transitiv_rel:
        # hier werden die rel mit den gleichen antecedent gezählt, die nicht selbst nicht (selbst exklusive)
        if  sum(1 for tupel in transitiv_rel if rel[0] == tupel[0]) > 1:
            
            #hier wird gmerged ({1}, {1,2},{1,3}), damit es später leichter wird um den graph zu generieren    
            ss_Pair = tuple([rel[0]]+[tupel[1] for tupel in transitiv_rel if rel[0] == tupel[0] ])
            
            #hier speichern wir diese Ordnung damit es sich nicht dupliziert 
            #hier speichern wir es so (({1},{1,2}), ({1},{1,3})), damit wir sie aus trans_rel entfernen können
            ss_rel = tuple([tupel for tupel in transitiv_rel if rel[0] == tupel[0]] )
            for elem in ss_rel: transitiv_rel.remove(elem)
            if ss_Pair not in same_antecedent : same_antecedent.extend([ss_Pair])
                    
        if  sum(1 for tupel in transitiv_rel if rel[1] == tupel[1]) > 1:
            st_pair = tuple([tupel[0] for tupel in transitiv_rel if rel[1]== tupel[1] ]+[rel[1]])
            st_rel = tuple([tupel for tupel in transitiv_rel if rel[1] == tupel[1] ])
            for elem in st_rel :transitiv_rel.remove(elem)
            if st_pair not in same_consequent :same_consequent.extend([st_pair])             
        
    
    rest.extend(transitiv_rel)
    #[({4}, {3, 4}), ({1, 4}, {1, 3, 4})]
    all = same_antecedent+same_consequent+rest
    
    
    
############## JZ GRAPH GENERIEREN ##################################
    g = grv.Graph('G', filename='process.gv', engine='sfdp')
    dot = grv.Digraph('digraph', comment='digraph')
    dot_src = """
    digraph {
       graph [pad="20,20" bgcolor=lightgray]
       node [style=filled]
       rankdir="BT"

    """    
    for ord in all:
        if ord in same_antecedent:
            for elem in ord[1:]:
                if len(ord[0])  > 1:
                    filtered_tuples = [tupel for tupel in all_targs if len(tupel) == len(ord[0])]
                    dot_src += f'    subgraph  {{ \n'
                    dot_src += f'    label="subgraph"; \n'
                    dot_src += f'rank = same; "{numToEntity(filtered_tuples[0])}";"{numToEntity(ord[0])}"; \n' 
                    #subgraphNodes.extend([ord[0]])    
                    dot_src += f'    }} \n'    
                    suCoVa = findeSupConfValue(graphDic,ord[0],elem) 
                    dot_src += f'    "{(numToEntity(ord[0]))}" -> "{(numToEntity(elem))}" [taillabel= "{suCoVa}" ] \n'
                else:
                    suCoVa = findeSupConfValue(graphDic,ord[0],elem) 
                    dot_src += f'    "{(numToEntity(ord[0]))}" -> "{(numToEntity(elem))}" [taillabel= "{suCoVa}" ] \n'
                
        if ord in same_consequent:
            for ele in ord[:-1]:
                suCoVa = findeSupConfValue(graphDic,ele,ord[-1]) 
                dot_src += f'    "{numToEntity(ele)}" -> "{numToEntity(ord[-1])}" [taillabel= "{suCoVa}" ] \n'
                
        if ord in rest :
            if len(ord[0])  > 1:
                filtered_tuples = [tupel for tupel in all_targs if len(tupel) == len(ord[0])]
                dot_src += f'    subgraph  {{ \n'
                dot_src += f'    label="subgraph"; \n'
                dot_src += f'rank = same; "{numToEntity(filtered_tuples[0])}";"{numToEntity(ord[0])}"; \n' 
                    #subgraphNodes.extend([ord[0]])    
                dot_src += f'    }} \n'
            suCoVa = findeSupConfValue(graphDic,ord[0],ord[1])   
            dot_src+= f'    "{numToEntity(ord[0])}"->"{numToEntity(ord[1])}" [taillabel= "{suCoVa}"] \n'        

          
    dot_src += '}\n'

    return dot_src
     
     
def numToEntity (elem):
    name = logName.split('_')[0] 
    if name == 'BPI2019':
        #BPI2019
        dicNum={'SRM: Created': 1, 'SRM: Complete': 2, 'SRM: Awaiting Approval': 3, 'SRM: Document Completed': 4, 'SRM: In Transfer to Execution Syst.': 5, 'SRM: Ordered': 6,
                'SRM: Change was Transmitted': 7, 'Create Purchase Order Item': 8, 'Vendor creates invoice': 9, 'Record Goods Receipt': 10, 'Record Invoice Receipt': 11, 'Clear Invoice': 12, 
                'Record Service Entry Sheet': 13, 'SRM: Transfer Failed (E.Sys.)': 14, 'Cancel Goods Receipt': 15, 'Vendor creates debit memo': 16, 'Cancel Invoice Receipt': 17, 'Change Delivery Indicator': 18, 
                'Remove Payment Block': 19, 'SRM: Deleted': 20, 'Change Price': 21, 'Delete Purchase Order Item': 22, 'SRM: Transaction Completed': 23, 'Change Quantity': 24, 'Change Final Invoice Indicator': 25, 
                'SRM: Incomplete': 26, 'SRM: Held': 27, 'Receive Order Confirmation': 28, 'Cancel Subsequent Invoice': 29, 'Reactivate Purchase Order Item': 30, 'Update Order Confirmation': 31, 'Block Purchase Order Item': 32, 
                'Change Approval for Purchase Order': 33, 'Release Purchase Order': 34, 'Record Subsequent Invoice': 35, 'Set Payment Block': 36, 'Create Purchase Requisition Item': 37, 'Change Storage Location': 38, 'Change Currency': 39, 
                'Change payment term': 40, 'Change Rejection Indicator': 41, 'Release Purchase Requisition': 42}
    if name == 'PreTravelCostLog':
        #travelCost     
        dicNum = {'Permit SUBMITTED by EMPLOYEE': 1, 'Permit FINAL_APPROVED by SUPERVISOR': 2, 'Request For Payment SUBMITTED by EMPLOYEE': 3, 
                'Request For Payment FINAL_APPROVED by SUPERVISOR': 4, 'Request For Payment REJECTED by MISSING': 5, 'Permit REJECTED by MISSING': 6, 
                'Request Payment': 7, 'Payment Handled': 8, 'Permit APPROVED by SUPERVISOR': 9, 'Permit FINAL_APPROVED by DIRECTOR': 10,
                'Request For Payment APPROVED by PRE_APPROVER': 11, 'Permit APPROVED by PRE_APPROVER': 12, 'Request For Payment REJECTED by PRE_APPROVER': 13,
                'Request For Payment REJECTED by EMPLOYEE': 14, 'Request For Payment APPROVED by SUPERVISOR': 15, 'Request For Payment FINAL_APPROVED by DIRECTOR': 16,
                'Permit REJECTED by PRE_APPROVER': 17, 'Permit REJECTED by EMPLOYEE': 18, 'Request For Payment REJECTED by SUPERVISOR': 19, 'Permit REJECTED by SUPERVISOR': 20,
                'Request For Payment SAVED by EMPLOYEE': 21, 'Request For Payment APPROVED by ADMINISTRATION': 22, 'Request For Payment APPROVED by BUDGET OWNER': 23, 'Request For Payment REJECTED by ADMINISTRATION': 24, 
                'Permit APPROVED by ADMINISTRATION': 25, 'Permit APPROVED by BUDGET OWNER': 26, 'Permit REJECTED by ADMINISTRATION': 27, 'Request For Payment REJECTED by BUDGET OWNER': 28, 'Permit REJECTED by BUDGET OWNER': 29}
    if name =='InternationalDeclarations':
        #InternationalDeclarations
        dicNum = {'Start trip': 1, 'End trip': 2, 'Permit SUBMITTED by EMPLOYEE': 3, 'Permit FINAL_APPROVED by SUPERVISOR': 4, 'Declaration SUBMITTED by EMPLOYEE': 5, 
                'Declaration FINAL_APPROVED by SUPERVISOR': 6, 'Request Payment': 7, 'Payment Handled': 8, 'Permit APPROVED by SUPERVISOR': 9, 'Permit FINAL_APPROVED by DIRECTOR': 10, 
                'Declaration APPROVED by PRE_APPROVER': 11, 'Declaration APPROVED by ADMINISTRATION': 12, 'Permit APPROVED by PRE_APPROVER': 13, 'Declaration REJECTED by PRE_APPROVER': 14, 
                'Declaration REJECTED by EMPLOYEE': 15, 'Declaration SAVED by EMPLOYEE': 16, 'Declaration REJECTED by MISSING': 17, 'Permit REJECTED by MISSING': 18, 
                'Declaration REJECTED by SUPERVISOR': 19, 'Declaration APPROVED by SUPERVISOR': 20, 'Declaration FINAL_APPROVED by DIRECTOR': 21, 'Permit REJECTED by PRE_APPROVER': 22, 
                'Permit REJECTED by EMPLOYEE': 23, 'Declaration REJECTED by DIRECTOR': 24, 'Permit REJECTED by SUPERVISOR': 25, 'Permit APPROVED by ADMINISTRATION': 26, 'Send Reminder': 27, 
                'Declaration APPROVED by BUDGET OWNER': 28, 'Declaration REJECTED by ADMINISTRATION': 29, 'Permit APPROVED by BUDGET OWNER': 30, 'Permit REJECTED by ADMINISTRATION': 31, 
                'Declaration REJECTED by BUDGET OWNER': 32, 'Permit REJECTED by BUDGET OWNER': 33, 'Permit REJECTED by DIRECTOR': 34}
    if name == 'PermitLog':
        #PermitLogErgb
        dicNum ={'Start trip': 1, 'End trip': 2, 'Permit SUBMITTED by EMPLOYEE': 3, 'Permit FINAL_APPROVED by SUPERVISOR': 4, 'Declaration SUBMITTED by EMPLOYEE': 5, 
                'Declaration FINAL_APPROVED by SUPERVISOR': 6, 'Request Payment': 7, 'Payment Handled': 8, 'Permit SAVED by EMPLOYEE': 9, 'Permit APPROVED by SUPERVISOR': 10, 
                'Permit FINAL_APPROVED by DIRECTOR': 11, 'Declaration APPROVED by PRE_APPROVER': 12, 'Declaration APPROVED by ADMINISTRATION': 13, 'Permit APPROVED by PRE_APPROVER': 14,
                'Declaration REJECTED by PRE_APPROVER': 15, 'Declaration REJECTED by EMPLOYEE': 16, 'Declaration SAVED by EMPLOYEE': 17, 'Send Reminder': 18, 'Request For Payment SUBMITTED by EMPLOYEE': 19,
                'Request For Payment FINAL_APPROVED by SUPERVISOR': 20, 'Request For Payment REJECTED by MISSING': 21, 'Permit REJECTED by MISSING': 22, 'Permit REJECTED by SUPERVISOR': 23,
                'Permit REJECTED by EMPLOYEE': 24, 'Request For Payment APPROVED by PRE_APPROVER': 25, 'Declaration REJECTED by MISSING': 26, 'Declaration APPROVED by SUPERVISOR': 27, 
                'Declaration FINAL_APPROVED by DIRECTOR': 28, 'Permit REJECTED by PRE_APPROVER': 29, 'Declaration REJECTED by DIRECTOR': 30, 'Declaration REJECTED by SUPERVISOR': 31, 
                'Request For Payment REJECTED by PRE_APPROVER': 32, 'Request For Payment REJECTED by EMPLOYEE': 33, 'Permit APPROVED by ADMINISTRATION': 34, 'Request For Payment REJECTED by SUPERVISOR': 35,
                'Request For Payment APPROVED by SUPERVISOR': 36, 'Request For Payment FINAL_APPROVED by DIRECTOR': 37, 'Declaration APPROVED by BUDGET OWNER': 38, 'Request For Payment SAVED by EMPLOYEE': 39,
                'Permit REJECTED by ADMINISTRATION': 40, 'Declaration REJECTED by ADMINISTRATION': 41, 'Permit APPROVED by BUDGET OWNER': 42, 'Declaration REJECTED by BUDGET OWNER': 43,
                'Request For Payment APPROVED by ADMINISTRATION': 44, 'Permit REJECTED by BUDGET OWNER': 45, 'Request For Payment APPROVED by BUDGET OWNER': 46, 'Request For Payment REJECTED by ADMINISTRATION': 47,
                'Request For Payment REJECTED by BUDGET OWNER': 48, 'Permit FOR_APPROVAL by ADMINISTRATION': 49, 'Permit REJECTED by DIRECTOR': 50, 'Permit FOR_APPROVAL by SUPERVISOR': 51}
    if name =='RequestForPayment':
        #request for payment
        dicNum={'Request For Payment SUBMITTED by EMPLOYEE': 1, 'Request For Payment FINAL_APPROVED by SUPERVISOR': 2, 'Request For Payment REJECTED by MISSING': 3, 'Request For Payment APPROVED by PRE_APPROVER': 4, 
                'Request Payment': 5, 'Payment Handled': 6, 'Request For Payment REJECTED by SUPERVISOR': 7, 'Request For Payment REJECTED by EMPLOYEE': 8, 'Request For Payment APPROVED by SUPERVISOR': 9, 'Request For Payment FINAL_APPROVED by DIRECTOR': 10, 
                'Request For Payment REJECTED by PRE_APPROVER': 11, 'Request For Payment SAVED by EMPLOYEE': 12, 'Request For Payment REJECTED by ADMINISTRATION': 13, 'Request For Payment APPROVED by ADMINISTRATION': 14, 'Request For Payment APPROVED by BUDGET OWNER': 15, 
                'Request For Payment REJECTED by BUDGET OWNER': 16, 'Request For Payment FOR_APPROVAL by ADMINISTRATION': 17, 'Request For Payment FINAL_APPROVED by BUDGET OWNER': 18, 'Request For Payment FOR_APPROVAL by SUPERVISOR': 19}
    
    if name == 'DomesticDeclarations':
        #domestic declerations
        dicNum={'Declaration SUBMITTED by EMPLOYEE': 1, 'Declaration FINAL_APPROVED by SUPERVISOR': 2, 'Request Payment': 3, 'Payment Handled': 4, 'Declaration APPROVED by PRE_APPROVER': 5, 'Declaration REJECTED by MISSING': 6, 'Declaration REJECTED by PRE_APPROVER': 7, 
                'Declaration REJECTED by EMPLOYEE': 8, 'Declaration SAVED by EMPLOYEE': 9, 'Declaration REJECTED by SUPERVISOR': 10, 'Declaration APPROVED by ADMINISTRATION': 11, 'Declaration APPROVED by BUDGET OWNER': 12, 'Declaration FOR_APPROVAL by SUPERVISOR': 13, 
                'Declaration REJECTED by ADMINISTRATION': 14, 'Declaration FOR_APPROVAL by PRE_APPROVER': 15, 'Declaration REJECTED by BUDGET OWNER': 16, 'Declaration FOR_APPROVAL by ADMINISTRATION': 17}

    nodeLabel= []
    
    for num in elem:        
        nodeLabel.extend(key for key, value in dicNum.items() if value == num)
    return nodeLabel

def findeSupConfValue(dic, antecedent, consequent):
    supConfvalue = ()
    max_supVal = max(int(value[0]) for key,value in dic.items())
    for key, value in dic.items():
        if str((antecedent,consequent)) == key :
            supConfvalue = (round(value[0]/max_supVal,2),round(value[1], 2))
    return supConfvalue

def is_transitiv(relations, all_targ):
    transRel = []
    rels = relations
    for rel1 in relations:
        for rel2 in relations:
            if (rel1[1] == rel2[0]):
                tranRel = tuple([rel1[0]]+[rel2[1]]) 
                transRel.extend([tranRel])
            #für reflexitivität
            if(rel2[0] == rel2[1] ):
                transRel.extend([rel2])
                
              
    for item in transRel: 
        if item in rels:rels.remove(item)
    return rels    


if __name__ == "__main__":
    path = r"C:\Users\Loli\BA\output.txt\BA\testresutl\2020PermitLog\PermitLog_minSup75_minConf50.txt"
    
    with open(path, "r") as file: 
        input_data = file.readlines()
   
   
    logName= path.split('\\')[-1].split('.')[0]
    dot_antecedent = extract_data(input_data,logName)
    graph = grv.antecedent(dot_antecedent)
    graph.render(filename=logName, format='png', cleanup=True, view=True)

  
    
