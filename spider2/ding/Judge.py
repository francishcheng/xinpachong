
import pandas as pd
import numpy as np
import time
from scipy.signal.signaltools import resample
import xlrd
import os
import xlwt
import copy
import pandas as pd
import csv
import sys
import numpy as np

from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def judge_youxiao(sj, C_ygz, Ce):
    sj = [int(i) for i in sj.split(',')[:-1]]
    sj = np.array([sj])
    sj = sj.T
    C_ygz=np.array([C_ygz])   ; #荧光值
    Ce=np.array([Ce])      ;#项目号
    sj_hang = len(sj) #350个数据点
    sj_lie = len(sj[0]) #数据条目数,1条
    reason=np.zeros((sj_lie,13))  #判定
    ##改变变量名
    curve2=sj
    curve2_lie=sj_lie
    curve2_hang=sj_hang
    yssj=np.zeros((sj_lie,sj_hang))
    yssj=sj#原始数据
    del sj
    del sj_lie
    del sj_hang#删除变量，释放缓存


    # 曲线数据光滑化,先光滑再归一化

    from scipy.signal import savgol_filter
    for i in range (curve2_lie):
        a = curve2[:,i]
        curve2[:,i]=savgol_filter(a,5,4)



    ##数据的归一化处理
    time_start = time.time() #开始计时

    curveToOne2=np.zeros((curve2_lie,curve2_hang))

    for i in range (curve2_lie):

        zxz=min(curve2.T[i]);
        zdz=max(curve2.T[i]);

        for j in range (curve2_hang):
            fenmu=(zdz-zxz)

            if fenmu==0:
                fenmu=0.1

            curveToOne2[i][j]=(curve2.T[i][j]-zxz)/fenmu

    curveToOne2=curveToOne2.T



    ##ce 的计算
    xiangmuhao=[0,0,1,1,1,5,3,1,1,1,1,2,1,0,0,1,1,1,1,1,1,1,1,1,2]

    ce=np.zeros((curve2_lie,1));#一维，且值都为1

    for i in range (curve2_lie):
        p=Ce[i]
        if (Ce[i]==33) or (Ce[i]==48)or (Ce[i]==49)or (Ce[i]==50)or (Ce[i]>24):
            p=3
            Ce[i]=p
        
        x=xiangmuhao[(p)] 
        ce[i]=x
        if (Ce[i]!=0) &(Ce[i]!=1) :
            reason[i][2]=1  #第九条无效判定标准，测试项目错误     


    ## 输入C、T1~T3参考值，从小到大输入！！
    ck=np.array([[190,290,0,0],[115,200,280,0],[67,146,217,294],[125,245,0,0],[65,180,305,0]])-1;# 4:老的单测;5:新三测
    sit_C=np.array([1,3,4,1,3]);     # C的位置

########################################################↓↓↓####################################################
 ########################################################↓↓↓####################################################
 ########################################################↓↓↓####################################################
 ########################################################↓↓↓####################################################
 ########################################################↓↓↓####################################################
 ########################################################↓↓↓####################################################
 ########################################################↓↓↓####################################################
 ########################################################↓↓↓####################################################   
    ##记录峰的出现位置f，判断峰的个数F
    error=[];
    bd=6;  #区间波动
    ad=[curveToOne2[curve2_hang-1]]
    for i in range (bd*2):#矩阵扩展
        curveToOne2=np.r_[curveToOne2, ad]

    h1=0.0025;  #峰区域的阈值 
    h2=0.01; #非峰区域的阈值

    f=np.zeros((len(curveToOne2),len(curveToOne2[1])));#记录是不是峰
    H=np.zeros((len(curveToOne2),len(curveToOne2[1])));
    F=np.zeros((len(curveToOne2[1]),2));
    dx=np.zeros((len(curveToOne2[1]),1));#非峰区域的均值，底线高度
    ff=np.zeros((len(curveToOne2),len(curveToOne2[1])));#1为峰区域，0为非峰区域


    #小功能：确定峰判断标准
     #输入
     #ck 4*4 整数 存放单双三单测的C位参考位点 
     #输出
     #H 356*706 整数 存放峰的高度标准
     #f 356*706 0 1整数 标记各曲线每一个位点上是否判别为峰


    # In[18]:


    ##波峰判别（波峰矫正）
    for j in range (curve2_lie):
        c=0
        d=0
        reason[j][10]=1
        for i in range(bd,curve2_hang+bd):    
            ## 确定峰判断标准
            h=h2; #高标准状态为非峰区域时候        
            p=ce[j]-1


            for ii in range (int(p)):

                if (ck[int(p)][ii]-20<=i) & (i<=ck[int(p)][ii]+20) & (curveToOne2[i][j]>0.3):  #i:处于参考峰区域时候，采用低标准
                    h=h1;

            H[i][j]=h;



            ## 顶峰判断
            if (curveToOne2[i][j]>(curveToOne2[i-bd][j]+H[i][j])) & (curveToOne2[i][j]>(curveToOne2[i+bd][j]+H[i][j])) & ((curveToOne2[i-1][j]<=curveToOne2[i][j])):

                if (i>40)& (i<320):#掐头去尾

                    a=(curveToOne2[i][j]-0.05)#此处的点的值-0.05
                    b=(curveToOne2[i-20][j]+curveToOne2[i+20][j])/2 #左右20处2个值的平均值
                    if (a<b)&(d!=0)&(i-d<50)&(i-d>5):

                        c=c+1#记录鼓包数量

                    if (a>=b):
                        f[i][j]=1;
                        f[i-1][j]=0;

                    d=i#记录上一个峰或鼓包的位置



        #判断是不是老单测标准    
        if ce[j]==1:
            findfind=f[:,j];
            if sum(f[:,j])>=2:
                sitfindfind=np.argwhere(findfind)
                if (abs(sitfindfind[0]-ck[3][0])<20) or (abs(sitfindfind[1]-ck[3][1])<20):
                    ce[j]=4;
            if sum(f[:,j])==1:
                sitfindfind=np.argwhere(findfind)
                if (abs(sitfindfind[0]-ck[3][0])<20):
                    ce[j]=4;                  
        #判断是不是新2测标准    
        if ce[j]==2:
            findfind=f[:,j];                       
            if sum(f[:,j])>=1:
                sitfindfind=np.argwhere(findfind)
                if (abs(sitfindfind[0]-ck[4][0])<30):
                    ce[j]=5;
        #判断是不是新2测标准    
        if ce[j]==5:
            findfind=f[:,j];                       
            if sum(f[:,j])>=1:
                sitfindfind=np.argwhere(findfind)
                if (abs(sitfindfind[0]-ck[1][0])<30):
                    ce[j]=2;       



       ## 结果统计
        F[j][0]=sum(f[:,j]);   #峰的个数

        #看鼓包
        if (c>=2) &(c<=7):
            reason[j][10]=0


    # In[ ]:


    ## 删除扩展的行 
    for i in range (bd*2):
        curveToOne2 = np.delete(curveToOne2, curve2_hang+bd*2-i-1, 0)  
        f= np.delete(f, curve2_hang+bd*2-i-1, 0)
        H= np.delete(H, curve2_hang+bd*2-i-1, 0)


    # In[ ]:


    sit=np.zeros((curve2_lie,7)); #储存峰的坐标
    sitliu=np.zeros((curve2_lie,7)); #储存峰的最终保留坐标
    sitc=np.zeros((len(curveToOne2[1]),1));#储存C峰位置
    sitc5=np.zeros((len(curveToOne2[1]),5));#储存C峰位置
    score=np.zeros((len(curveToOne2[1]),5));#储存5个项目分别的得分
    paixu=np.zeros((curve2_lie,7))#储存峰的排序信息
    feng=np.zeros((curve2_lie,7)); #合适峰的原始数据
    jianju=np.zeros((curve2_lie,3)) #记录间距，最多3个间距
    ff1=np.zeros((curve2_lie,4));#记录四个位点是否有峰 单测
    ff2=np.zeros((curve2_lie,4));#记录四个位点是否有峰 双测
    ff3=np.zeros((curve2_lie,4));#记录四个位点是否有峰 三测
    ff4=np.zeros((curve2_lie,4));#记录四个位点是否有峰 老单测
    ff5=np.zeros((curve2_lie,4));#记录四个位点是否有峰 老双测


    # In[ ]:


    def findce(j):##留下有用的峰

        if (F[j][0]>=2)&(F[j][0]<=7):#读出来至少两个峰 才执行
            #先找间距
            a=0
            b=1
            d=0#间距的个数
            for i in range (14):#最多找7次间距
                if b==a:
                    b=a+1
                if b==7:
                    break   
                if a==7:
                    break               
                if (sit[j][a]==0)&(sit[j][b]==1):
                    a=b
                    continue
                if (sit[j][a]==0)&(sit[j][b]==0):
                    b=b+1
                    a=b
                    continue
                if (sit[j][a]==1)&(sit[j][b]==1):
                    b=b+1
                    continue


                if (sit[j][a]!=0) & (sit[j][b]!=0):

                    c=abs(sit[j][b]-sit[j][a])#距离

                    if (c>=50) :
                        #jianju[j][d]=c
                        #d=d+1

                        sitliu[j][b]=sit[j][b]

                        sitliu[j][a]=sit[j][a]

                        a=b

                        b=b+1

                    if c<50:

                        if (a==0) or (a>=5):#在最左边或最右边
                            if(feng[j][a]<=feng[j][b]):
                                feng[j][a]=0               
                                sit[j][a]=0
                                if c<20:
                                    reason[j][10]=0
                            if(feng[j][a]>feng[j][b]):
                                feng[j][b]=0               
                                sit[j][b]=0
                                if c<20:
                                    reason[j][10]=0
                        if (a>0) & (a<4)&(b<6):
                            zjz=(sit[j][a-1]+sit[j][b+1])/2
                            x=abs(zjz-sit[j][a])
                            y=abs(zjz-sit[j][b])

                            if x>=y:
                                feng[j][a]=0               
                                sit[j][a]=0
                                if c<20:
                                    reason[j][10]=0
                            if x<y:
                                feng[j][b]=0               
                                sit[j][b]=0
                                if c<20:
                                    reason[j][10]=0


                        b=b+1

                    if c>150:
                        a=a+1




            f[:,j]=0#峰的重新矫正
            for i in range (7):
                if sitliu[j][i]!=0:
                    k=sitliu[j][i]
                    f[int(k),j]=1
                    ff[i-30:i+30,j]=1#记录峰区域

            F[j][0]=sum(f[:,j]);   #峰的个数统计


       #间距重新算


    # In[ ]:


    def findff(j):   
        qz1=1   #权重1，峰高度排序乘的系数
        qz2=4   #权重2，C线有峰加的分
        qz3=1 #权重3，平均距离倒数乘的系数
        qz4=2   #权重4，符合要求的峰的个数的权重
        p=F[j][0]
        if F[j][0]>7:
            p=7
        sitc[j]=0
        kk=0#计算平均偏差
        k=0#计算平均偏差
        m=0
        x=0

        for m in range (int(p)): #单双三测 判断C、T1~T3位点是否有峰


            if  (ce[j]==1)&(sit[j][m]!=0):
                for x in range (4):
                    if  (abs(sit[j][m]-ck[0][x])<=20):
                        kk=kk+1
                        k=k+(abs(sit[j][m]-ck[0][x]))
                        ff1[j][x]=1;  #记录位点m是否出现峰
                        score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz1/(paixu[j][m]+1)
                        if x==0:
                            sitc[j]=sit[j][m]#记录C线峰坐标
                            sitc5[j][0]=sit[j][m]
                            score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz2
                if k!=0:
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk
                if k==0:
                    k=1
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk  
                continue              


            if  (ce[j]==2)&(sit[j][m]!=0):
                for x in range (4):
                    if  (abs(sit[j][m]-ck[1][x])<=20):
                        kk=kk+1
                        k=k+(abs(sit[j][m]-ck[1][x]))                         
                        ff2[j][x]=1;  #记录位点m是否出现峰
                        score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz1/(paixu[j][m]+1)
                        if x==2:
                            sitc[j]=sit[j][m] 
                            sitc5[j][1]=sit[j][m]                        
                            score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz2  
                if k!=0:
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk 
                if k==0:
                    k=1
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk                  
                continue

            if  (ce[j]==3)&(sit[j][m]!=0):
                for x in range (4):
                    if  (abs(sit[j][m]-ck[2][x])<=20):

                        kk=kk+1
                        k=k+(abs(sit[j][m]-ck[2][x]))                        
                        ff3[j][x]=1;  #记录位点m是否出现峰
                        score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz1/(paixu[j][m]+1) 

                        if x==3:
                            sitc[j]=sit[j][m]
                            sitc5[j][2]=sit[j][m]                        
                            score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz2 
                if k!=0:
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk
                if k==0:
                    k=1
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk                

                continue 


            if  (ce[j]==4)&(sit[j][m]!=0):
                for x in range (4):
                    if  (abs(sit[j][m]-ck[3][x])<=20):
                        kk=kk+1
                        k=k+(abs(sit[j][m]-ck[3][x]))                         
                        ff4[j][x]=1;  #记录位点m是否出现峰
                        score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz1/(paixu[j][m]+1)  

                        if x==0:
                            sitc[j]=sit[j][m]
                            sitc5[j][3]=sit[j][m]
                            score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz2
                if k!=0:
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk                  
                if k==0:
                    k=1
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk                       
                continue


            if  (ce[j]==5)&(sit[j][m]!=0):
                for x in range (4):
                    if  (abs(sit[j][m]-ck[4][x])<=20):

                        kk=kk+1
                        k=k+(abs(sit[j][m]-ck[4][x]))                        
                        ff5[j][x]=1;  #记录位点m是否出现峰
                        score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz1/(paixu[j][m]+1) 

                        if x==2:
                            sitc[j]=sit[j][m]
                            sitc5[j][4]=sit[j][m]
                            score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz2 
                if k!=0:
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk  
                if k==0:
                    k=1
                    score[j][int(ce[j])-1]=score[j][int(ce[j])-1]+qz3*(kk/k)+qz4*kk                  
                continue                       


    # In[ ]:


    for j in range (curve2_lie):

        if F[j][0]<=7: #一定要小于等于7个峰 才执行
            k=0
            for i in range (curve2_hang):#记录7个峰的坐标
                if f[i][j]==1:    
                    sit[j][k] = i 
                    k=k+1;



    for j in range (curve2_lie):

        for m in range (7):#记录sit坐标下的峰值
            feng[j][m]=yssj[int(sit[j][m])][j]



        paixu[j]=np.argsort(-feng[j,:])

        findce(j)#看看是否有鼓包，并且把有效的峰留下来


    # In[ ]:


    #记录7峰以内的峰坐标信息

    for j in range (curve2_lie):
        if F[j][0]<=7: #一定要小于等于7个峰 才执行
            k=0
            for i in range (curve2_hang):
                if f[i][j]==1:    
                    sit[j][k] = i 
                    k=k+1;

    sitc=np.zeros((len(curveToOne2[1]),1));

    for j in range (curve2_lie):
        p=F[j][0]
        if F[j][0]>7:
            p=7
        for m in range (int(p)-2):
            if (sit[j][m]!=0)&(sit[j][m+1]!=0)&(sit[j][m+2]!=0):
                if  (abs(sit[j][m]-sit[j][m+1])<=50)&(abs(sit[j][m+1]-sit[j][m+2])<=50):
                    sit[j][m+1]=0 
                    reason[j][10]=0
        findff(j)   


    # In[ ]:


    #测试项目选错的纠正。
    for j in range (curve2_lie):


        p=F[j][0]
        if F[j][0]>7:
            p=7   
        k=ce[j]+1
        if ce[j]==4:
            k=2
        if ce[j]==5:
            k=3

        F[j][1]=max(sum(ff1[j,:]),sum(ff2[j,:]),sum(ff3[j,:]),sum(ff4[j,:]),sum(ff5[j,:]))   #有效峰的个数

        if (sitc[j]!=0) & (F[j][0]==k):#C值峰处有峰，且总峰数小于等于ce+1 则不执行这一步
            continue
        if (F[j][0])<=0:
            continue#只有一个峰或无峰的也不继续执行


    #分别计算5种情况下峰的情况 
        score[j,:]=0
        ce[j]=1
        findff(j)
        ce[j]=2
        findff(j)
        ce[j]=3
        findff(j)
        ce[j]=4
        findff(j)
        ce[j]=5
        findff(j)

        a = score[j]
        b=np.where(a==np.max(a))
        ce[j]=b[0][0]+1  #ce 与实际保持一致
        sitc[j]=sitc5[j][int(ce[j]-1)]

        F[j][1]=max(sum(ff1[j,:]),sum(ff2[j,:]),sum(ff3[j,:]),sum(ff4[j,:]),sum(ff5[j,:]))   #有效峰的个数


    # In[ ]:


    #判断有效无效
    true=np.zeros((curve2_lie,1))
    leibie=np.zeros((curve2_lie,1))
    for j in range (curve2_lie):
    ## 关卡判断
        p=ce[j]+1
        if ce[j]==4:
            p=2
        if ce[j]==5:
            p=3

        # 纵坐标MAX大于10000 否则是空跑
        reason[j][0]=1;    
        #if max(yssj[:,j])<=10000:
        if sum(yssj[:,j]<12500)>curve2_hang*0.9:
            reason[j][0]=0;  #空跑   


        if (F[j][1]<=p)&(F[j][1]>=1)&(F[j][0]<=7): #一定要小于等于7个峰
            reason[j][1]=1;#记录失效原因，1表示通过。第二关卡：峰数匹配。


        if C_ygz[j]>=75: #有效试剂检测
            reason[j][4]=1;#⑤	荧光值>=75，或C线有峰。
        if sitc[j]!=0:
            reason[j][4]=1

        reason[j][3]=1    
        if (F[j][1]==4)&(abs(int(ce[j])-xiangmuhao[int(Ce[j])])!=0): 
            reason[j][3]=0;#第4关卡：测试项目选错
        if (int(ce[j])-xiangmuhao[int(Ce[j])]>0)& (F[j][1]==ce[j]+1): 
            reason[j][3]=0;#第4关卡：测试项目选错


        k=F[j][0]-1
        if F[j][0]>7:
            k=6

        if (F[j][1]>1)& (sum(curveToOne2[int(sit[j][0]):int(sit[j][int(k)]),j]>0.5)<0.9*abs(int(sit[j][0])-int(sit[j][int(k)]))):
            reason[j][6]=1;#第7关卡；最左边到最右边的峰之间，不能90%以上的高于0.4
        if (F[j][1]<=1):
            reason[j][6]=1


        reason[j][8]=1   # reason[j][8]=1#是否出现骤降


        sumff=0
        x=0
        for i in range(curve2_hang):  
            if ff[i][j]==0:
                sumff=sumff+curveToOne2[i][j];
                x=x+1
        if x!=0:
            dx[j]=sumff/x;#非峰区域的均值，底线高度
        for i in range(curve2_hang):  
            if  (i>=20)&(i<300):
                if(curveToOne2[i][j]>=curveToOne2[i+50][j]+0.15):
                    if (curveToOne2[i+50][j]<=0.05)&(max(curveToOne2[i+50:curve2_hang,j])<0.05)&(yssj[i+50][j]<5000):
                        reason[j][8]=0
                        if (ce[j]==3) or (ce[j]==5) :
                            if i >280:
                                reason[j][8]=1#未查到底或插反
        reason[j][12]=1#非峰区域底线足够低
        if (ce[j]==1):
            if (sum(curveToOne2[0:125,j]>0.235)<60)&(np.mean(curveToOne2[0:125,j])<0.235): 
                reason[j][5]=1;
            if (dx[j]>0.3):
                reason[j][12]=0; #非峰区域底线足够低                     
            if sum(curveToOne2[320:340,j])<20*0.35:
                reason[j][7]=1;  #8:尾巴不能高 (第七关) 
        if (ce[j]==4):
            if (sum(curveToOne2[0:90,j]>0.235)<60)&(np.mean(curveToOne2[0:90,j])<0.235): 
                reason[j][5]=1;#第6关卡；底线要低，不然就是受潮了,  0~30处不能全都大于0.235
            if sum(curveToOne2[320:340,j])<20*0.35:
                reason[j][7]=1;  #8:尾巴不能高 (第七关)             

        if (ce[j]==2)or (ce[j]==5) :
            if sum(curveToOne2[0:30,j]>0.5)<25: 
                reason[j][5]=1;#第6关卡；底线要低，不然就是受潮了,  0~30处不能全都大于0.5
            if sum(curveToOne2[320:340,j])<20*0.5:
                reason[j][7]=1;  #8:尾巴不能高 (第七关) 
        if (ce[j]==3)  :
            if sum(curveToOne2[0:30,j]>0.75)<25: 
                reason[j][5]=1;#第6关卡；底线要低，不然就是受潮了,  0~-30处不能全都大于0.75
            if sum(curveToOne2[320:340,j])<20*0.70:
                reason[j][7]=1;  #8:尾巴不能高 (第七关)                              



        reason[j][11]=1#是否出现左边的直线（跑板不充分）            
        if(sum(yssj[0:200,j]<15000)>75)&(np.mean(curveToOne2[200:349,j])>0.05)&(ce[j]!=1)&(ce[j]!=4):  #左边出现直线且右边有峰      
            reason[j][11]=0#是否出现左边的直线（跑板不充分）

        if (ce[j]!=1):
            if(np.mean(curveToOne2[175:349,j])-np.mean(curveToOne2[0:175,j])>0.37)&(np.mean(curveToOne2[0:175,j])<0.05):  #左半区平均值比右半区平均值小0.37,且左半区足够低
                reason[j][11]=0#是否出现左边的直线（跑板不充分）

        if(np.mean(curveToOne2[250:349,j])-np.mean(curveToOne2[0:249,j])>0.37)&(np.mean(curveToOne2[0:249,j])<0.05):  #左半(0-250)区平均值比右半区平均值小0.37,且左半区足够低
            reason[j][11]=0#是否出现左边的直线（跑板不充分）


        reason[j][9]=1#是否加样太少,此项的条件为其他项不全为1
        if (ce[j]==1) or (ce[j]==4):
            if(sum(reason[j,0:9])+sum(reason[j,10:13])<12):
                if (max(yssj[:,j])<35000)  or  (np.mean(yssj[:,j])<25000):
                    if(np.mean(curveToOne2[200:349,j])>0.05):#(右边有峰)
                        reason[j][9]=0


        if (ce[j]==3):
            if   (np.mean(yssj[:,j])<50000) & ((max(yssj[:,j])<100000))&(sum(reason[j,0:9])+sum(reason[j,10:13])<12):
                if(np.mean(curveToOne2[200:349,j])>0.05):
                    reason[j][9]=0

        if (ce[j]==2) or (ce[j]==5):
            if (sum(reason[j,0:9])+sum(reason[j,10:13])<12):
                if   (np.mean(yssj[:,j])<30000) & ((max(yssj[:,j])<35000))&(sum(reason[j,0:9])+sum(reason[j,10:13])<12):
                    if(np.mean(curveToOne2[200:349,j])>0.05):
                        reason[j][9]=0


    ## 有效判断+有效类型判断

        if sum(reason[j])==len(reason[j]): #得分=关卡数（全对）
            true[j]=1; #有效

 ##############################################################################################################################
 ##############################################################################################################################
##############################################################################################################################
 ##############################################################################################################################

    #分类：

    reason_s = ''
    explain = ''
    for i in range  (len(curveToOne2[0])):

        if (true[i]==1):#有效
            reason_s += "有效"
            continue

        if (true[i]==0):  #无效

            if (reason[i][0]==0):
                reason_s += "空跑"
                explain +="请将试剂卡板加样后按正确的方向插入"
                continue              

            if (reason[i][10]==0)&(sum(reason[i,:])==12):
                reason_s += "鼓包"
                explain +="读数过程中请勿移动试纸条"          
                continue

            if (reason[i][2]==0):
                reason_s += "无效项目"
                explain +="请选择正确的项目号"          
                continue     
            if (reason[i][3]==0)&(sum(reason[i,:])==12):
                reason_s += "选错项目"
                explain +="请选择正确的项目号"        
                continue       

            if (reason[i][5]==0)&(sum(reason[i,:])>=11):
                reason_s += "头部翘起"
                explain +="请清洗毛发后重新检测"        
                continue        
            if (reason[i][6]==0)&(sum(reason[i,:])>=11):
                reason_s += "中间过高"
                explain +="请清洗毛发后重新检测"            
                continue           
            if (reason[i][7]==0)&(sum(reason[i,:])>=11):
                reason_s += "尾部翘起"
                explain +="请清洗毛发后重新检测"         
                continue                   

            if (sum(reason[i,5:8])<=1)&(sum(reason[i,:])>=10):
                reason_s += "受潮"
                explain +="卡板在空气中暴露的时间过长"          
                continue 


            if (reason[i][8]==0)&(reason[i][0]==1)&(reason[i][11]==1):
                reason_s += "未插到底或插反"
                explain +="试剂卡板错位，请以正确的方式插入"          
                continue 


            if (reason[i][9]==0)&(reason[i][0]==1)&(reason[i][11]==1)&(reason[i][8]==1):
                reason_s += "滴样太少"
                explain +="请滴入足量的裂解液"           
                continue

            if (reason[i][11]==0)&(reason[i][0]==1)&(reason[i][8]==1): 
                reason_s += "跑板时间太短"
                explain +="请耐心等待试剂卡板跑板完成后再读数"          
                continue

            if (reason[i][1]==0)&(reason[i][0]==1):
                reason_s += "无C线"
                explain +="未检测到质控线，请再测一次"           
                continue 

            if (reason[i][4]==0):
                reason_s += "无C线"
                explain +="未检测到质控线，请再测一次"          
                continue     

            if (reason[i][12]==0)&(sum(reason[i,:])==12):
                reason_s += "受潮"
                explain +="卡板在空气中暴露的时间过长"           
                continue             

            #others ，其他错误类型
            reason_s += "其他错误"
            explain +="数据无效，请再测一次"          
            continue
            


    return int(true), reason, reason_s, explain

if __name__ == '__main__':
    
    xm='  甲基安非他明/吗啡'
    Ce='ABCC'
    #输入荧光值
    C_ygz=1223
    ##输入 1*350的数据 curve2=np.array([1,2,3,……,350])
    #例：curve2=np.array([1,2,3,4,51,56,1564,564,987,98,5])
    curve2=np.array([45028,44985,44977,44970,44955,44992,45035,45043,45050,45065,45038,45004,44983,44946,44906,44871,44837,44798,44774,44744,44713,44675,44654,44608,44568,44530,44489,44425,44380,44335,44281,44243,44233,44204,44180,44169,44146,44109,44086,44057,44047,44014,44003,43991,43991,43983,44031,44058,44109,44157,44223,44242,44286,44327,44367,44387,44456,44506,44567,44625,44699,44744,44797,44856,44916,44971,45047,45121,45173,45234,45300,45370,45423,45481,45544,45600,45649,45757,45916,46127,46431,46859,47388,48047,48918,49967,51295,52909,54941,57348,60290,63721,67825,72559,78079,84409,91709,99987,109414,120107,132231,145937,161445,178949,198595,220479,244577,270745,298674,327943,358021,388273,418034,446597,473267,497379,518411,535889,549467,558932,564172,565103,561735,554155,542507,527008,508000,485913,461257,434593,406561,377761,348802,320287,292716,266524,242076,219618,199231,180952,164653,150163,137267,125755,115419,106133,97746,90188,83404,77348,71968,67294,63249,59797,56887,54499,52506,50912,49623,48614,47812,47213,46761,46486,46361,46393,46613,47024,47623,48467,49549,50938,52623,54743,57282,60401,64103,68587,73842,80052,87251,95565,105062,115882,128119,141935,157509,174982,194556,216326,240368,266577,294778,324567,355495,386935,418254,448756,477758,504573,528601,549289,566196,578965,587404,591370,590845,585894,576695,563416,546376,525942,502516,476570,448682,419410,389352,359131,329363,300578,273261,247791,224423,203260,184289,167395,152388,139047,127132,116458,106866,98213,90410,83409,77157,71599,66743,62521,58918,55841,53279,51117,49329,47837,46631,45642,44877,44313,43936,43758,43747,43940,44324,44929,45753,46897,48309,50104,52251,54885,57968,61673,66029,71212,77234,84320,92532,102005,112866,125241,139147,154624,171624,190035,209698,230416,251909,273871,295912,317670,338677,358507,376708,392886,406602,417573,425536,430341,431909,430275,425518,417781,407272,394212,378895,361642,342810,322803,302062,281014,260078,239633,220015,201474,184203,168305,153871,140854,129212,118846,109647,101492,94262,87848,82155,77121,72651,68719,65292,62313,59740,57554,55724,54195,52940,51961,51169,50546,50059,49712,49424,49209,49046,48900,48762,48605,48488,48343,48200,48039,47882,47662,47403,47087,46680,46173,45534,44773,43871,42802])
    curve2 = np.zeros(150)

    ret = judge_youxiao(curve2, Ce, C_ygz, xm)
    print(ret)
    