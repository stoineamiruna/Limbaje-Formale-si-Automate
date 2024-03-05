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
                sectiune.append(linie)
            linie = f.readline()
            linie = linie.rstrip("\n")
    sectiuni[cheie]=sectiune
    ls=[]
    if "Rules" in sectiuni:
        for r in sectiuni["Rules"]:
            ls2 = r.split("->")
            m=ls2[1].split(",")
            ls.append((ls2[0],m))
        sectiuni["Rules"]=ls
    return sectiuni
def load_sections(fisier):
    sectiuni=task(fisier)
    if "Vars" not in sectiuni:
        return []
    if "Sigma" not in sectiuni:
        return []
    if "Rules" not in sectiuni:
        return []
    ls=[]
    for sectiune in sectiuni:
        ls.append(sectiune)
    if len(ls)!=3:
        return []
    return ls

def load_vars(fisier):
    sectiuni=task(fisier)
    if "Vars" not in sectiuni:
        return []
    ls=[]
    for v in sectiuni["Vars"]:
        var=v.split(",")
        ls.append(var[0])
        if var[0].islower()!=0:
            return []
    return ls

def load_sigma(fisier):
    sectiuni=task(fisier)
    if "Sigma" not in sectiuni:
        return []
    ls=[]
    for l in sectiuni["Sigma"]:
        ls.append(l)
    return ls

def load_start(fisier):
    sectiuni=task(fisier)
    if "Vars" not in sectiuni:
        return []
    if len(sectiuni["Vars"])==0:
        return []
    if len(sectiuni["Vars"])==1:
        if sectiuni["Vars"][0][-1:]!="*":
            return []
        else:
            return [sectiuni["Vars"][0]]
    lsS=[]
    for var in sectiuni["Vars"]:
        if var[-1]=='*':
            lsS.append(var[:-2])
    if len(lsS)!=1:
        return []
    return lsS[0]

def load_rules(fisier):
    sectiuni=task(fisier)
    if "Rules" not in sectiuni:
        return []

    for regula in sectiuni["Rules"]:
        if regula[0] not in load_vars(fisier):
            return []
        for cuv in regula[1]:
            if cuv not in sectiuni["Sigma"] and cuv not in load_vars(fisier):
                return []
    return sectiuni["Rules"]
''''
print(task("exemplu0"))
print(load_sections("exemplu0"))
print(load_sigma("exemplu0"))
print(load_vars("exemplu0"))
print(load_rules("exemplu0"))
print(load_start("exemplu0"))
'''

def CFG1(fisier,cuv):
    if load_sections(fisier)==[] or load_sigma(fisier)==[] or load_vars(fisier)==[] or load_rules(fisier)==[]:
        return -1
    d=task(fisier)
    for rg in d["Rules"]:
        s=rg[0]
        reg=" ".join(rg[1])
        if s in cuv:
            cuv =cuv.replace(s,reg)
    for var in load_vars(fisier):
        if var in cuv:
            return CFG1(fisier,cuv)
    return cuv

def CFG2(fisier,prop):
    if load_sections(fisier)==[] or load_sigma(fisier)==[] or load_vars(fisier)==[] or load_rules(fisier)==[]:
        return -1
    d=task(fisier)
    Rules = load_rules(fisier)
    for rg in Rules:
        prop_nou=[]
        starea1=rg[0]
        starea2=rg[1]
        for cv in prop:
            if cv==starea1:
                prop_nou.extend(starea2)
            else:
                prop_nou.append(cv)
        prop=prop_nou

    for var in load_vars(fisier):
        if var in prop:
            return CFG2(fisier,prop)

    cuv=" ".join(prop)
    return cuv

#prima varianta, in care, dandu-se un cuvant, variabilele se vor inlocui in ordinea in care apar in
#sectiunea respectiva din fisierul dat (nu ia in considerare cazul in care o variabila respezinta un subsir din
#alta variabila prezenta
#De exemplu: fisierul exemplu3, in care sunt prezente atat variabilele NP si N

print(CFG1("exemplu0","0A1"))
print(CFG1("exemplu1","0A1"))
print(CFG1("exemplu2","EXPR"))
print(CFG1("exemplu3","S"))
print(CFG1("exemplu4","COMMAND"))

#varianta 2, care ia in considerare cazul particular de mai sus, dar, in schimb, primeste ca parametru din prima o lista
#prin care sunt delimitate variabilele unele de altele

print(CFG2("exemplu0",["0","A","1"]))
print(CFG2("exemplu1",["0","A","1"]))
print(CFG2("exemplu2",["EXPR"]))
print(CFG2("exemplu3",["S"]))
print(CFG2("exemplu4",["COMMAND"]))