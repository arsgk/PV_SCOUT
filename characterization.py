

def characterize(shapes_list,issue_list):

    temp=40
   
    
    for shapes in shapes_list:
        #print(shapes)


        if shapes =='square' and temp >35 and temp <45 :
            issue= "Optical Degradation"
            issue_list.append(issue)
        
        if shapes =='rectangle' and temp >35 and temp <45 :
            issue= "Cell Crack-Burned cell"
            issue_list.append(issue)            
            
        if shapes =='square' and temp >45 and temp <55 :
            issue= "Cell Crack-Burned cell"
            issue_list.append(issue)
            
        if shapes =='rectangle' and temp >45 and temp <55 :
            issue= "Cell Crack-Burned cell"
            issue_list.append(issue)


        if shapes =='square' and temp >55 and temp <65 :
            issue= "Potential Induced Degradation (PID)"
            issue_list.append(issue)

        if shapes =='rectangle' and temp >55 and temp <65 :
            issue= "Potential Induced Degradation (PID)"
            issue_list.append(issue)

      
        if shapes =='square' and temp >65 and temp <150 :
            issue= "Shading-Faulty Interconnections"
            issue_list.append(issue)
            
    
        if shapes =='rectangle' and temp >65 and temp <150 :
            issue= "Faulty interconnection-Broken interconnection"
            issue_list.append(issue)
    

    