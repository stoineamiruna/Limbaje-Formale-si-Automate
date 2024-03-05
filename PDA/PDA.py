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
            ls.append((ls2[0],ls2[1],ls2[2],ls2[3],ls2[4]))
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
    if "Gama" not in sectiuni:
        return []
    ls=[]
    for sectiune in sectiuni:
        ls.append(sectiune)
    if len(ls)!=4:
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

def load_gama(fisier):
    sectiuni=task(fisier)
    if "Gama" not in sectiuni:
        return []
    ls=[]
    for litera in sectiuni["Gama"]:
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
        if stare[-3:]=='S,F':
            lsS.append(stare[:-4])
            lsF.append(stare[:-4])
        else:
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
        if ls[0] in sectiuni["States"] and ls[4] in sectiuni["States"] and ls[2] in sectiuni["Gama"] and ls[1] in sectiuni["Sigma"] and ls[3] in sectiuni["Gama"]:
            actiuni.append(tuple(ls))
    return actiuni


def PDA_recursiv(d, lsF, lsS, str, s_c, stiva):

    if len(lsS)!=1:
        return 0
    if str=="":
        c=""
    else:
        c=str[0]
    if c!= "" and c not in d["Sigma"]:
        return 0
    nr=0
    for act in d["Actions"]:
        si=act[0]
        sf=act[4]
        pop=act[2]
        push=act[3]
        chr=act[1]

        if si==s_c:
            if chr=='E':
                if pop=='E':
                    scop=stiva
                    if push!='E':
                        scop.append(push)

                    if len(str)>=1:
                        nr=nr+PDA_recursiv(d,lsF,lsS,str,sf, scop)
                    if sf in lsF and str == "" and stiva == []:
                        nr += 1
                elif len(stiva)>0 and pop==stiva[len(stiva)-1]:
                    scop=stiva[:-1]
                    if push!='E':
                        scop.append(push)

                    if len(str)>=0:
                        nr=nr+PDA_recursiv(d,lsF,lsS,str,sf,scop)
                    if sf in lsF and str=="" and scop==[]:
                        nr= nr+ 1


            elif chr==c:
                if pop=='E':
                    scop=stiva
                    if push!='E':
                        scop.append(push)

                    if len(str)>1:
                        nr=nr+PDA_recursiv(d,lsF,lsS, str[1:],sf,scop)
                    elif len(str)==1:
                        nr = nr + PDA_recursiv(d, lsF, lsS, "", sf, scop)
                    if sf in lsF and str=="" and stiva==[]:
                        nr += 1


                elif len(stiva)>0 and pop==stiva[len(stiva)-1]:

                    scop=stiva[:len(stiva)-1]
                    if push!='E':
                        scop.append(push)

                    if len(str)>1:
                        nr=nr+PDA_recursiv(d,lsF,lsS, str[1:],sf,scop)
                    elif len(str)==1:
                        nr = nr + PDA_recursiv(d, lsF, lsS, "", sf, scop)

                    if sf in lsF and str=="" and stiva==[]:
                        nr += 1

    return nr

def emulate_PDA(fisier, str):
    if load_actions==[] or load_states(fisier)==[] or load_sigma(fisier)==[] or load_sections(fisier)==[] or load_gama(fisier)==[]:
        return -1
    d = task(fisier)
    lsF, lsS = load_states(fisier)
    s_c=lsS[0]
    stiva=[]
    return PDA_recursiv(d,lsF,lsS, str, s_c, stiva)


str1="00"
str2="01"
str3="0011"
str4="10"
str5="000111"
str6="0101"

print(emulate_PDA("exemplu1",str1))
print(emulate_PDA("exemplu1",str2))
print(emulate_PDA("exemplu1",str3))
print(emulate_PDA("exemplu1",str4))
print(emulate_PDA("exemplu1",str5))
print(emulate_PDA("exemplu1",str6))

str7="abc"
str8="aabcc"
str9="abbccc"
print(emulate_PDA("exemplu2",str7))
print(emulate_PDA("exemplu2",str8))
print(emulate_PDA("exemplu2",str9))

str10="000"
str11="011011"
str12="01010"
str13="1"
str14="101101"
print(emulate_PDA("exemplu3",str10))
print(emulate_PDA("exemplu3",str11))
print(emulate_PDA("exemplu3",str12))
print(emulate_PDA("exemplu3",str13))
print(emulate_PDA("exemplu3",str14))

'''
In solutia data, am inlocuit folosirea caracterului 'ε' cu 'E' deoarece aveam erori in interpretarea acestui caracter de catre compliator
(cel putin asta se intampla pe dispozitivul meu)
'''