import time
import sys
import copy

global vars
vars={}

for i in range(9):
    tmp_row=[]
    for j in range(9):
        tmp_col=[]
        for k in range(1,10):
            tmp_col.append(None)
        tmp_row.append(tmp_col)
    vars[i]=tmp_row

def makeCSP(filename,string):
    row=0
    if string==False and filename!=False:
        f=open(filename,'r')
        for line in f:
            content=line.split(' ')
            for i in range(len(content)):
                content[i]=content[i][0]
            for i  in range(len(content)):
                if i%9==0 and i!=0:
                    row+=1
                if content[i]=='0':
                    vars[row][i%9]=[x for x in range(1,10)]
                else:
                    vars[row][i%9]=[int(content[i])]
    elif string!=False and filename==False:
        content=string.split(' ')
        for i in range(len(content)):
            content[i]=content[i][0]
        for i in range(len(content)):
            if i%9==0 and i!=0:
                row+=1
            if content[i]=='0':
                vars[row][i%9]=[x for x in range(1,10)]
            else:
                vars[row][i%9]=[int(content[i])]


    display_partialcsp(vars)

def checkrow(csp,row,col,num):
    for i in range(9):
        if num in csp[row][i] and len(csp[row][i])==1:
            return False
    return True

def checkcol(csp,row,col,num):
    for i in range(9):
        if num in csp[i][col] and len(csp[i][col])==1:
            return False
    return True

def checkgrid(csp,row,col,num):
    r=0
    r=row
    c=0
    c=col
    while (r%3)!=0:
        r-=1
    while (c%3)!=0:
        c-=1
    for i in range(r,r+3):
        for j in range(c,c+3):
            if num in csp[i][j] and len(csp[i][j])==1:
                return False
    return True

def checkconstraint(csp,row,col,num):
    if checkrow(csp,row,col,num) and checkcol(csp,row,col,num) and checkgrid(csp,row,col,num):
        return True
    else:
        return False

def iszero(csp):
    if any(len(csp[i][j])>1 for i in range(9) for j in range(9)):
        return True
    else:
        return False

def findzero(csp):
    min_length=10
    min_x=9
    min_y=9
    for i in range(9):
        for j in range(9):
            if len(csp[i][j])<min_length and len(csp[i][j])>1:
                min_length=len(csp[i][j])
                min_x=i
                min_y=j
    return min_x,min_y

def get_neighbors(row,col):
    list_neighbors=[]
    #Neighbors in the same row
    for i in range(9):
        if i!=col:
            list_neighbors.append((row,i))

    #Neighbors in the same col
    for i in range(9):
        if i!=row:
            list_neighbors.append((i,col))

    #Neighbors(remaining) in the same 3*3 grid
    r=0
    r=row
    c=0
    c=col
    while (r%3)!=0:
        r-=1
    while (c%3)!=0:
        c-=1
    for i in range(r,r+3):
        for j in range(c,c+3):
            if (i,j) not in list_neighbors and i!=row and j!=col:
                list_neighbors.append((i,j))

    return list_neighbors

def CP(csp,r,c,val):
    temp_vars=copy.deepcopy(csp)
    neighbors=get_neighbors(r,c)

    to_be_removed=[]
    for v in temp_vars[r][c]:
        if v != val:
            to_be_removed.append(v)
    temp_vars[r][c]=[val]
    csp=copy.deepcopy(temp_vars)
    for n in neighbors:
        if val in temp_vars[n[0]][n[1]]:
            temp_vars[n[0]][n[1]].remove(val)
            if len(temp_vars[n[0]][n[1]])==0:
                return False
            elif len(temp_vars[n[0]][n[1]])==1:
                if not checkconstraint(csp,n[0],n[1],temp_vars[n[0]][n[1]][0]):
                    return False
                else:
                    t=preprocess(csp)
                    if t!=False:
                        temp_vars=t

    all_units=[]
    row_units=[]
    col_units=[]
    grid_units=[]
    for row in range(9):
        row_units.append((row,c))
    for col in range(9):
        col_units.append((r,col))
    tr=0
    tr=r
    tc=0
    tc=c
    while (tr%3)!=0:
        tr-=1
    while (tc%3)!=0:
        tc-=1
    for i in range(tr,tr+3):
        for j in range(tc,tc+3):
            grid_units.append((i,j))
    all_units.append(row_units)
    all_units.append(col_units)
    all_units.append(grid_units)

    for val2 in to_be_removed:
        for u in all_units:
            has_val=[]
            for a in u:
                if not (a in has_val):
                    if val2 in temp_vars[a[0]][a[1]]:
                        has_val.append(a)
            if len(has_val)==1:
                return CP(temp_vars,has_val[0][0],has_val[0][1],val2)

    return temp_vars

def preprocess(csp):
    for r in range(9):
        for c in range(9):
            if len(csp[r][c])==1:
                val=csp[r][c][0]
                neighbors=get_neighbors(r,c)
                for n in neighbors:
                    if val in csp[n[0]][n[1]]:
                        csp[n[0]][n[1]].remove(val)
                        if len(csp[n[0]][n[1]])==0:
                            return False
    return csp

def BT(csp):
    global vars
    r=0
    c=0
    if not iszero(csp):
        return True
    else:
        f0=findzero(csp)
        r,c=f0[0],f0[1]
    init_value={}
    init_value=copy.deepcopy(csp)
    neighbors=get_neighbors(r,c)
    for i in csp[r][c]:
        if True:
            f=CP(csp,r,c,i)
            if f==False:
                csp=init_value

            elif f!=False:
                vars=f

                if BT(vars):
                    return vars
    return False

def display_fullcsp(csp):
    for r in range(9):
        for c in range(9):
            print csp[r][c],
        print
    print

def display_partialcsp(csp):
    for r in range(9):
        for c in range(9):
            if len(csp[r][c])==1:
                print csp[r][c],
            else:
                print [0],
        print
    print

def solvepuzzle(filename,string):
    global vars
    makeCSP(filename,string)
    vars=preprocess(vars)
    if vars==False:
        print
        print '#'*15,'NO SOLUTION','#'*15
        print
        print False
        print
    else:
        print
        print 'After preprocessing'
        print
        print '#'*15,'SUDOKU','#'*15
        display_fullcsp(vars)
        print
        res=BT(vars)

        if res:
            print
            print '#'*15,'SOLUTION EXISTS','#'*15
            print
            display_fullcsp(vars)

        else:
            print
            print '#'*15,'NO SOLUTION','#'*15
            print
            display_fullcsp(vars)
            print

def solvecases(filename,string):
    start=time.time()
    solvepuzzle(filename,string)
    duration=time.time()-start
    print 'Duration(seconds):',duration
    print

if __name__=='__main__':
    if len(sys.argv)>1:
        print
        print '#'*15,'SUDOKU','#'*15
        print
        if sys.argv[1]=='r' and len(sys.argv)>2:
            print 'The puzzle is:',sys.argv[2]
            print
            solvecases(filename=False,string=sys.argv[2])
        elif sys.argv[1]=='r' and len(sys.argv)==2:
            print 'The string representing the puzzle not provided'
            print
        elif sys.argv[1]=='f' and len(sys.argv)>2:
            print 'The puzzle is:',sys.argv[2]
            print
            solvecases(filename=sys.argv[2],string=False)
        elif sys.argv[1]=='f' and len(sys.argv)==2:
            print 'Filename not provided'
            print
        elif sys.argv[1]!='r' and sys.argv[1]!='f':
            print 'Appropriate input not found'
            print
    elif len(sys.argv)==1:
        print
        print '#'*15,'SUDOKU','#'*15
        print
        print 'More inputs required'
        print