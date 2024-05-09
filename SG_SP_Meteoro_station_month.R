#Sugar cane_per meteorological station month
#validation data more than 1 soil type
#First, load the SoilR package
library(SoilR)

#AUXILIAR Library
library(data.table)
library(datasets)
library("xlsx")
library (deSolve)
library(readxl)

#Mude para o arquivo com os dados. De preferencia deixar no mesma pasta.Necessário definir o tipo de dados em col_types

CLIMA1 <- read_excel("D:/Desktop/Task and Research/Mestrado/data bank/CLIMA_SP.xlsx", 
                     col_types = c("numeric","text","text","numeric", "numeric", "numeric", "numeric","numeric",
                                   "numeric","numeric","numeric","numeric","numeric","text")
                     ,sheet = "MAIN 1")

CAL <-read_excel("D:/Desktop/Task and Research/Mestrado/PPGMSA/validação do modelo/SPCALmonth.xls",
                 col_types = c("text","numeric","numeric","numeric","numeric","numeric","numeric",
                               "numeric","numeric","numeric","numeric","text"), sheet = "S1_main")

#atribuição de dados 
data1 <- c(CLIMA1)
data3 <- c(CAL)

#data frame
Sv1<- function(na, i){
  namev = c("Av M Temp( °C)","Eto mm/month Calc","Rain mm/month")
  d = data1[[namev[na]]]
  return(d[i])
}

Sv2<- function(na, i){
  namev = c("ID-A","SOLO 1","SOLO 2","SOLO 3","SOLO 4","SOLO 5","SOLO 6","SOLO 7")
  d = data1[[namev[na]]]
  return(d[i])
}

CALI <-function(na,i){
  namev = c("1","2","3","4","5","6","7","8","9","10")
  d = data3[[namev[na]]]
  return(d[i])
}

# Create an empty list to store the vectors
vector_list <- list()

# Set up the loop to create 12 vectors
for (z in 1:7) {
  # Generate the start and end values for this vector
  start_value <- ((z - 1) * 6) + 1
  end_value <- z * 6
  
  # Create the vector by concatenating the values using the c() function
  new_vector <- c(start_value:end_value)
  
  # Add the completed vector to the list
  vector_list[[z]] <- new_vector
}

#Escolhe um valor único por lista
Si<- function(na, i){
  d = vector_list[[na]]
  return(d[i])
}

S1 = c(1,2,3,0,5,6,7,8,0,10)
S2 = c(0,2,0,0,0,6,7,8,0,10)
S3 = c(1,2,0,4,0,6,7,8,9,10)
S4 = c(0,2,3,4,5,0,0,0,9,10)
S5 = c(1,0,3,4,5,0,0,0,9,10)
S6 = c(1,2,0,0,0,0,0,0,9,0)
S7 = c(1,0,0,0,0,0,0,0,0,0)
Sts = list(S1,S2,S3,S4,S5,S6,S7)

St<- function(na, i){
  d = Sts[[na]]
  return(d[i])
}

# Create an empty list to store the vectors
vector_listn <- list()

# Set up the loop to create 12 vectors
for (z in 1:10) {
  # Generate the start and end values for this vector
  start_valuen <- ((z - 1) * 12) + 1
  end_valuen <- z * 12
  
  # Create the vector by concatenating the values using the c() function
  new_vectorn <- c(start_valuen:end_valuen)
  
  # Add the completed vector to the list
  vector_listn[[z]] <- new_vectorn
}

#Escolhe um valor único por lista
Sn<- function(na, i){
  d = vector_listn[[na]]
  return(d[i])
}

#Soil cover factor
#SCF=data.frame(Month=1:12, sc=c(0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1, 1, 1, 0.6, 0.6))
#bb = data.frame(Month=1:12, sc=c(FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE))
#############################################################################################
#rothC otimizado para mes
B <- list()
xpi = c()
xpii = c()
xpiii = c()
for (x in 1:3){
  for (i in seq_along(Sts)) {
    B[[i]] <- numeric(length(Sts[[i]]))
    for (a in seq_along(Sts[[i]])) {
      if (St(i, a) != 0) {

        fT=fT.RothC(Temp = c(Sv1(1,Sn(a,))[1:12]))
        fW=fW.RothC(P=c(Sv1(3,Sn(a,))[1:12]), E=c(Sv1(2,Sn(a,))[1:12]), S.Thick = 30, pClay = Sv2(i+1,2), pE = 0.75, bare = FALSE)$b
        
        # Constantes de decomposição dos pools do RothC
        kDPM = 10
        kRPM = 0.3
        kBIO = 0.66
        kHUM = 0.02
        
        #climate modifield
        years=seq(0, 20, by=1/12) 
        
        #climate modified  decomposition constant --- can be changed #SCF[,2]
        CDIex=data.frame(years,rep(fT*fW,length.out=length(years)))
    
        #Cenarios
        alf = 0.03  #proporção de biochar tradado como material organico fresco
        Ibi = c((2.46*0.814), (1.23*0.814), (0.62*0.814)) # adição de biochar em t c/ ha ano com percas de 0.059 por lixiviação e 0.15 por erosão
        Io = c(6.57, 9.74, 11.1) #c(3.17, 6.33, 7.71) #porporção para o modelo
        
        #entrada para o RothC
        Irothc = 0.95*Io[x]+Ibi[x]*alf
        
        # constante de decomposição do biochar no RBC
        kbioc= 0.00119 
        
        #RothC paper test soil 1 without Biochar In = Io,
        RCarbon<- function(invro){
          return(RothCModel(t=years,
                            ks = c(k.DPM = kDPM, k.RPM = kRPM, k.BIO = kBIO, k.HUM = kHUM, k.IOM = 0),
                            C0 = c(CALI(a,Si(i, ))[1], CALI(a,Si(i, ))[2], CALI(a,Si(i, ))[3], CALI(a,Si(i, ))[4], CALI(a,Si(i, ))[5]),
                            In = Irothc+CALI(a,Si(i, ))[6],
                            FYM = 0,
                            DR = 1.44,
                            clay = Sv2(i+1,2),
                            xi = CDIex,
                            solver = deSolve.lsoda.wrapper,
                            pass = FALSE))
        }
        
        ExR=RCarbon(t)  #RothC
        Ctr=getC(ExR)      #RothC retorna os valores para cada pool
        Rt=getReleaseFlux(ExR)     #Liberação de Carbono DE CADA POOL_ only additional information
        
        #Modelo de decomposição do biochar
        Biomod <- function(t, y, parms){
          with(as.list(c(y, parms)),{
            dcb<- (1-alf)*Ibc-kbioc*cb
            list(dcb)})
        }
        y<- c(cb=0)
        parms<- c(alf=0.03, kbioc=0.00119, Ibc=Ibi[x])
        t<-seq(0, 20, by=1/12)
        
        outB <- ode(y, t, Biomod, parms)
        
        # soma todos os pools em um só
        Totn <- rowSums(Ctr)
        Biot <- (outB)
        
        #sumt = (Biot[22:42] + Totn)
        sumt = data.frame(Biot[(length(t)+1):length(Biot)] + Totn)
        #-------------------------------------------------------------------------------
        B[[i]][a] <- list(data.frame(sumt))
      } else {
        
        B[[i]][a] <- 0 
      }
    }
  }
  
  xpi[x] = (list(B))
  
}

#-------------------------------------------------------------------------------
################## escrever no excel ###########################################
write.xlsx(xpi, file= "D:/Desktop/Task and Research/Mestrado/PPGMSA/Carbon modeling/Reproducibility/Data/TES3.xls", sheetName="Cenários", append=TRUE) 

