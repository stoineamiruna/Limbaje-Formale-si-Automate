def task(fisier):
    sectiuni = {}
    with open(fisier) as f:
        linie=f.readline()
        linie=linie.rstrip("\n")
        ct=0
        while linie!="":
            if linie[0]=='[' and linie[-1]==']':
                if ct!=0:
                    sectiuni[cheie]=sectiune
                cheie = linie[1:len(linie) - 1]
                ct+=1
                sectiune=[]
            else:
                if linie[0]!='#':
                    ls=linie.split("#")
                    sectiune.append(ls[0])
            linie = f.readline()
            linie = linie.rstrip("\n")
    sectiuni[cheie]=sectiune
    ls=[]
    if "Actions" in sectiuni:
        for act in sectiuni["Actions"]:
            ls2=act.split(",")
            ls.append((ls2[0],ls2[1],ls2[2]))
        sectiuni["Actions"]=ls
    return sectiuni
def load_sections(fisier):
    sectiuni=task(fisier)
    if "Sigma" not in sectiuni:
        return []
    if "States" not in sectiuni:
        return []
    if "Actions" not in sectiuni:
        return []
    ls=[]
    for sectiune in sectiuni:
        ls.append(sectiune)
    if len(ls)!=3:
        return []
    return ls

def load_sigma(fisier):
    sectiuni=task(fisier)
    if "Sigma" not in sectiuni:
        return []
    ls=[]
    for litera in sectiuni["Sigma"]:
        ls.append(litera)
    return ls

def load_states(fisier):
    sectiuni=task(fisier)
    if "States" not in sectiuni:
        return []
    if len(sectiuni["States"])==0:
        return []
    if len(sectiuni["States"])==1:
        if sectiuni["States"][0][-3:]!="S,F":
            return []
        else:
            return [sectiuni["States"][0]]
    lsF=[]
    lsS=[]
    for stare in sectiuni["States"]:
        if stare[-1]=='S':
            lsS.append(stare[:-2])
        if stare[-1] == 'F':
            lsF.append(stare[:-2])
    if len(lsS)!=1 or len(lsF)<1:
        return []
    return (lsF,lsS)

def load_actions(fisier):
    sectiuni=task(fisier)
    if "Actions" not in sectiuni:
        return []
    actiuni=[]
    for actiune in sectiuni["Actions"]:
        ls = actiune.split(",")
        if ls[0] in sectiuni["States"] and ls[2] in sectiuni["States"] and ls[1] in sectiuni["Sigma"]:
            actiuni.append(tuple(ls))
    return actiuni


def nfa_recursiv(d, lsF, lsS, str, s_c):
    c = str[0]
    if str=="":
        return 0
    if len(lsS)!=1:
        return 0
    c=str[0]
    if c not in d["Sigma"]:
        return 0
    nr=0
    for act in d["Actions"]:
        if act[0]==s_c and act[1]==c:
            if len(str)>1:
                nr=nr+nfa_recursiv(d, lsF, lsS, str[1:], act[2])
            else:
                if act[2] in lsF:
                    nr=nr+1
        elif act[0]==s_c and act[1]=='E':
            if len(str)>=1:
                nr=nr+nfa_recursiv(d, lsF, lsS,str, act[2])
            else:
                if act[2] in lsF:
                    nr+=1
    return nr

def emulate_nfa(fisier, str):
    if load_actions==[] or load_states(fisier)==[] or load_sigma(fisier)==[] or load_sections(fisier)==[]:
        return -1
    d = task(fisier)
    lsF, lsS = load_states(fisier)
    s_c=lsS[0]
    return nfa_recursiv(d,lsF,lsS, str, s_c)


str1="101"
str2="100110"
str3="1101"
str4="1001"
str5="111"
print(emulate_nfa("exemplu1", str1))
print(emulate_nfa("exemplu1", str2))
print(emulate_nfa("exemplu1", str3))
print(emulate_nfa("exemplu1", str4))
print(emulate_nfa("exemplu1", str5))

print(emulate_nfa("exemplu2", str1))
print(emulate_nfa("exemplu2", str2))
print(emulate_nfa("exemplu2", str3))
print(emulate_nfa("exemplu2", str4))
print(emulate_nfa("exemplu2", str5))

'''
In solutia data, am inlocuit folosirea caracterului 'ε' cu 'E' deoarece aveam erori in interpretarea acestui caracter de catre compliator
(cel putin asta se intampla pe dispozitivul meu)
'''