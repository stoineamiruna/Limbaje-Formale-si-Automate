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


def emulate_dfa(fisier, str):
    d = task(fisier)
    lsF,lsS=load_states(fisier)
    s_c=lsS[0]
    for c in str:
        if c not in d["Sigma"]:
            return 0
        s_n=""
        for act in d["Actions"]:
            if act[0]==s_c and act[1]==c:
                s_n=act[2]
        if s_n=="":
            return 0
        s_c=s_n
    if s_c in lsF:
        return 1
    return 0

str1="000010"
str2="00100"
str3="101001"
str4="10100100"

''''
print(emulate_dfa("exemplu1", str1))
print(emulate_dfa("exemplu1", str2))
print(emulate_dfa("exemplu1", str3))
print(emulate_dfa("exemplu1", str4))

print(emulate_dfa("exemplu2", str1))
print(emulate_dfa("exemplu2", str2))
print(emulate_dfa("exemplu2", str3))
print(emulate_dfa("exemplu2", str4))

'''
'''
def emulate_nfa(d, str, s_i, lsF):
    for c in str:
        if c not in d["Sigma"]:
            return 0
        s_n=""
        print(s_c)
        for act in d["Actions"]:
            if act[0]==s_c and act[1]==c:
                s_n=act[2]
                emulate_dfa(d, str[:-1], s_n)
        if s_n=="":
            return 0
        s_c=s_n
    if s_c in lsF:
        return 1
    return 0
lsF,lsS=load_states("exemplu2")
s_i=lsS[0]
print(emulate_nfa(d,str5, ))
#de fct nfa-ul ca tema (cred)
'''
def nfa_recursiv(d, lsF, lsS, str, s_c):
    c = str[0]
    if str=="":
        return 0
    if len(lsS)!=1:
        return 0
    c=str[0]
    if c not in d["Sigma"]:
        return 0
    print(s_c)
    nr=0
    for act in d["Actions"]:
        if act[0]==s_c and act[1]==c:
            if len(str)>1:
                nr=nr+nfa_recursiv(d, lsF, lsS, str[1:], act[2])
            else:
                print(act[2])
                if act[2] in lsF:
                    nr=nr+1
        elif act[0]==s_c and act[1]=='ε':
            if len(str)>1:
                nr=nr+nfa_recursiv(d, lsF, lsS,str, act[2])
            else:
                print(act[2])
                if act[2] in lsF:
                    ct=ct+1
                    nr+=1
    return nr

def emulate_nfa(fisier, str):
    d = task(fisier)
    lsF, lsS = load_states(fisier)
    s_c=lsS[0]
    return nfa_recursiv(d,lsF,lsS, s_c)


str1="101"
print(emulate_nfa("exemplu1", str1))