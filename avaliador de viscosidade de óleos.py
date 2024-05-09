import pandas as pd
from sklearn.metrics import r2_score
import xlsxwriter
from matplotlib import pyplot as plt
import numpy as np
#avaliar em quais temperaturas eles performam melhor

data = pd.read_excel(r'C:\Users\paulo\Desktop\Task and Research\GPMT\scripts gpmt\viscmodeling.xlsx')
df1 = pd.DataFrame(data, columns=['API at 15 °C'])
df2 = pd.DataFrame(data, columns=['T(°C)'])
df3 = pd.DataFrame(data, columns=['uexp(cp)'])

x = df3['uexp(cp)'].count()

API = [df1.loc[i, 'API at 15 °C'] for i in range(x)]
T = [df2.loc[i, 'T(°C)'] for i in range(x)]
uod = [df3.loc[i, 'uexp(cp)'] for i in range(x)]
Tf= [((T[i]*(9/5))+32) for i in range(x)]
Trr= [((T[i]+273.15)*(9/5)) for i in range(x)]
TC = T
i = 0

lisD=['Beal (1946)','Bennison (1998) - Form1','Bennison (1998) - Form2','Elsharkawy and Alikhan (1999)','Elsharkawy and Gharbi (2001)','Hossain et al.(2005)','Kartoatmodjo and Schmidt (1994)','Labedi (1992)','McCain (1991)','Naseri et al.(2005)','Naseri et al.(2012)','Egbogah-Jacks','Modified Egbogah-Jacks (Extra-Heavy Oils)','Modified Egbogah-Jacks (Heavy Oils)','Oyedeko and Ulaeto (2013)','Petrosky and Farshad (1995)','Ulaeto and Oyedeko (2014)','Standing(1942)']
#'De Ghetto et al. (1995)' - 4
from OilViscosity import ViscOilUndDead_Beal, ViscOilUndDead_BennF1, \
    ViscOilUndDead_BennF2, ViscOilUndDead_DeGhetalExHy, ViscOilUndDead_Alik, \
    ViscOilUndDead_ElsndGhar, ViscOilUndDead_Hossetal, ViscOilUndDead_KartndSchm, \
    ViscOilUndDead_Labed, ViscOilUndDead_McC91, ViscOilUndDead_Nasetal5, \
    ViscOilUndDead_Nasetal12, ViscOilUndDead_EgboJack, ViscOilUndDead_ModEgboJackExHy, ViscOilUndDead_ModEgboJackHy, \
    ViscOilUndDead_OyedndUlae, ViscOilUndDead_PetrndFarsh,  \
    ViscOilUndDead_UlandOye, ViscOilUndDead_Stand

func = lambda i,keyword='bar':(i,keyword)
correlation = [lambda i:ViscOilUndDead_Beal(API[i], Trr[i], x),
               lambda i:ViscOilUndDead_BennF1(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_BennF2(API[i], Tf[i], x), #               lambda i:ViscOilUndDead_DeGhetalExHy(API[i],Tf[i],x),
               lambda i:ViscOilUndDead_Alik(API[i], Trr[i], x),
               lambda i:ViscOilUndDead_ElsndGhar(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_Hossetal(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_KartndSchm(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_Labed(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_McC91(API[i], Trr[i], x),
               lambda i:ViscOilUndDead_Nasetal5(Trr[i], API[i], x),
               lambda i:ViscOilUndDead_Nasetal12(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_EgboJack(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_ModEgboJackExHy(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_ModEgboJackHy(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_OyedndUlae(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_PetrndFarsh(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_UlandOye(API[i], Tf[i], x),
               lambda i:ViscOilUndDead_Stand(API[i], Tf[i], x)]

'''
for a in range(len(correlation)):
    for i in range(x):
        if correlation[a](i) == None:
            print(lisD[a])
            del(correlation[a])
    print(a)
'''

#AAE
apnd = []
for a in range(len(correlation)):
        apd = []
        for i in range(x):
            apd.append(abs(correlation[a](i)-uod[i])) #-uod[i]))
        apnd.append((sum(apd)/x))

#AARD_A
apndi = []
for a in range(len(correlation)):
        apdi = []
        for i in range(x):
            apdi.append(abs(((correlation[a](i) - uod[i])/uod[i])*100))
        apndi.append((sum(apdi) / x))

#AARD_Value
apndii = []
for a in range(len(correlation)):
        apdii = []
        for i in range(x):
            apdii.append(abs(((correlation[a](i) - uod[i])/uod[i])*100))
        apndii.append((sum(apdii) / x))

#Dead
Rank2 = []
for i in range(3):
    if i==0:
        Rank2.append((min(apndi)))
    elif i >= 1:
        del(apndi[apndi.index(min(apndi))])
        Rank2.append((min(apndi)))

deadsat = []
for i in range(3):
    if Rank2[i] in apndii:
        deadsat.append(apndii.index(Rank2[i]))
    else:
        print('false', Rank2[i])

#UndDead
VD1=[correlation[deadsat[0]](i) for i in range(x)]
VD2=[correlation[deadsat[1]](i) for i in range(x)]
VD3=[correlation[deadsat[2]](i) for i in range(x)]

#plt.plot(100,100,'k-')
uds = [uod[i]*(1.2) for i in range(x)]
udi = [uod[i]*(0.8) for i in range(x)]

plt.figure(1)
plt.plot(uds,uod,'k--')
plt.plot(udi,uod,'k--')
plt.plot(uod,uod,'k-')
plt.plot(VD1,uod, 'go', markersize=1, label =lisD[deadsat[0]])
plt.plot(VD2,uod, 'bo', markersize=1, label =lisD[deadsat[1]])
plt.plot(VD3,uod, 'ro', markersize=1, label =lisD[deadsat[2]])
plt.xlim(0,1400)
plt.ylim(0,1400)
plt.title('Visc - Experimental(cp) vs Calculado')
plt.xlabel('Visc-calculado(cp)')
plt.ylabel('Visc - Experimental(cp)')
plt.legend(loc='best')
plt.savefig('plot1.png', dpi=300, bbox_inches='tight')

plt.figure(2)
plt.plot(uds,uod,'k--')
plt.plot(udi,uod,'k--')
plt.plot(uod,uod,'k-')
plt.plot(VD1,uod, 'go', markersize=2, label =lisD[deadsat[0]])
plt.xlim(0,1400)
plt.ylim(0,1400)
plt.title('Visc - Experimental(cp) vs Calculado')
plt.xlabel('Visc-calculado(cp)')
plt.ylabel('Visc - Experimental(cp)')
plt.legend(loc='best')
plt.savefig('plot2.png', dpi=300, bbox_inches='tight')

plt.figure(3)
plt.plot(uds,uod,'k--')
plt.plot(udi,uod,'k--')
plt.plot(uod,uod,'k-')
plt.plot(VD2,uod, 'bo', markersize=2, label =lisD[deadsat[1]])
plt.xlim(0,1400)
plt.ylim(0,1400)
plt.title('Visc - Experimental(cp) vs Calculado')
plt.xlabel('Visc-calculado(cp)')
plt.ylabel('Visc - Experimental(cp)')
plt.legend(loc='best')
plt.savefig('plot3.png', dpi=300, bbox_inches='tight')

plt.figure(4)
plt.plot(uds,uod,'k--')
plt.plot(udi,uod,'k--')
plt.plot(uod,uod,'k-')
plt.plot(VD3,uod, 'ro', markersize=2, label =lisD[deadsat[2]])
plt.xlim(0,1400)
plt.ylim(0,1400)
plt.title('Visc - Experimental(cp) vs Calculado')
plt.xlabel('Visc-calculado(cp)')
plt.ylabel('Visc - Experimental(cp)')
plt.legend(loc='best')
plt.savefig('plot4.png', dpi=300, bbox_inches='tight')


R = []
for a in range(len(correlation)):
    corr = []
    for i in range(x):
        corr.append(correlation[a](i))
    R.append(r2_score(corr,uod))
    del(corr)

for t in range(1):
    outWorkbook4 = xlsxwriter.Workbook("Avalição da viscosidade DEAD petro.xlsx")
    outSheet4 = outWorkbook4.add_worksheet()
    outSheet4.write('A1', 'Correlações DEAD')
    outSheet4.write('B1', 'AARD')
    outSheet4.write('C1','R²')
    outSheet4.write('D1', 'Melhores Correlações óleo morto')
    outSheet4.write('D2', lisD[deadsat[0]])
    outSheet4.write('D3', lisD[deadsat[1]])
    outSheet4.write('D4', lisD[deadsat[2]])
    for c in range(1):
        if c == 0:
            for v in range(len(correlation)):
                outSheet4.write(v + 1, 0, lisD[v])
                outSheet4.write(v + 1, 1, apndii[v])
                outSheet4.write(v+1, 2, R[v])
    outWorkbook4.close()





for t in range(1):
    outWorkbook4 = xlsxwriter.Workbook("Avalição da viscosidade MOG T vs Erro petro.xlsx")
    outSheet4 = outWorkbook4.add_worksheet()
    outSheet4.write('A1', 'T(°C)')
    outSheet4.write('B1', 'API')
    for c in range(len(correlation)):
        outSheet4.write(0, c+2, lisD[c])
        for v in range(x):
            if c == 0:
                outSheet4.write(v + 1, 0, T[v])
                outSheet4.write(v + 1, 1, API[v])
            outSheet4.write(v + 1, c+2, abs(correlation[c](v)))
    outWorkbook4.close()

'''

cor = []
for i in range(x):
    cor.append(correlation[7](i))

plt.figure(9)
plt.plot(uds,uod,'k--')
plt.plot(udi,uod,'k--')
plt.plot(uod,uod,'k-')
plt.plot(cor,uod, 'ro', markersize=2, label =lisD[7])
plt.title('Visc - Experimental(cp) vs Calculado')
plt.xlabel('Visc-calculado(cp)')
plt.ylabel('Visc - Experimental(cp)')
plt.legend(loc='best')
plt.savefig('plot9.png', dpi=300, bbox_inches='tight')

print(apndii[7],lisD[7])


plt.figure(4)
plt.plot(4000,4000,'k-')
plt.plot(uod,VD1, 'go', markersize=2, label =lisD[deadsat[0]])
plt.plot(uod,VD2, 'bo', markersize=2, label =lisD[deadsat[1]])
plt.plot(uod,VD3, 'ro', markersize=2, label =lisD[deadsat[2]])
plt.xlim(0,4000)
plt.ylim(0,4000)
plt.title('oil')
plt.xlabel('Visc-calculado')
plt.ylabel('Visc-experimental')
plt.legend(loc='best')
plt.savefig('plot5.png', dpi=300, bbox_inches='tight')
'''