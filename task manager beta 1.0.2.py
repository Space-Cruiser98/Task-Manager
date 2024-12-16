task=[[1,7,9],[2,3,7],[3,4,5],[4,9,2]]
start=[0,]
end=[]
start2=[]
end2=[0]
t=0
i=0

while True :
    if (task[i][1]== 0 and task[i][2]==0) :
        i+=1
    else :
        start.append(t)
        for j in range(1,6):
            task[i][1]-=1
            t+=1
            if task[i][1]==0:
                break
        end.append(t)
        if (task[i][2]>0 and task[i][1]==0):
            if start2==[]:
                t=end[-1]
            else:
                t=end2[-1]
            start2.append(t)
            for k in range(1,task[i][2]+1) :
                task[i][2]-=1
                t+=1
                if task[i][2]==0:
                    break
            end2.append(t)
    i+=1
    if i == len(task):
        i=0
    t=end[-1]
    c=0
    for F in task :
        if F[1]==0 and F[2]==0 :
            c+=1
    if c == len(task):
        break
print (task,start,end,start2,end2)


