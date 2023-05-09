

def severity_state(severity_state_list,shapes_list,dT_PV):

    
    
    for shapes in shapes_list:
        #print(shapes)
        if dT_PV >35 and dT_PV <45:
            severity_state='Small Fault'
            severity_state_list.append(severity_state) 

        if dT_PV >45 and dT_PV <55 :
            severity_state='Medium Fault'
            severity_state_list.append(severity_state) 

        if dT_PV >55 and dT_PV <65:
            severity_state='Major Fault'
            severity_state_list.append(severity_state) 

        if dT_PV >65:
            severity_state='Critical Fault'
            severity_state_list.append(severity_state) 