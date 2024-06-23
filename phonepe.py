import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import requests
import json
import os

#connection to database
import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",password="",)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("create database if not exists newphonepe")
mycursor.execute("use newphonepe")

#stremlit Part
st.set_page_config(page_title="PhonePe DV&E",
                   page_icon="☔",
                   layout="wide")
st.image("C:/Users/DELL XPS/Pictures/Screenshots/pp.png",width=1000)
st.title(":rainbow[PhonePe Data Visualization and Exploration]")

with st.sidebar:
    select=option_menu("Menu",["Home","Explore Data","Insights","KeyPoints"])

if select=="Home":
    st.title(":violet[ABOUT PHONEPE]")
    col1,col2=st.columns([2,4])
    with col1:
        st.image("C:/Users/DELL XPS/Downloads/ppimg.jpeg")
    with col2:
        st.link_button("PhonePe.com","http://www.phonepe.com/")
        st.write('''PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India.
                  PhonePe was founded in December 2015,by Sameer Nigam, Rahul Chari and Burzin Engineer.The PhonePe app, based on the Unified Payments Interface (UPI),
                  went live in August 2016.The PhonePe app is accessible in 11 Indian languages.It enables users to perform various financial transactions such as sending and receiving money, 
                  recharging mobile and DTH, making utility payments, conducting in-store payments.''')
    st.image("C:/Users/DELL XPS/Downloads/www.phonepe.com_about-us_.png")

#Aggregated transaction details

path1="C:/Blast/PortableGit/pulse/data/aggregated/transaction/country/india/state/"
Agg_tran_list=os.listdir(path1) # returns a list of filenames in a specified directory. 
                                #It retrieves the names of all files and directories within the specified path

clm1={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}
for i in Agg_tran_list:
    pi1=path1+i+"/"
    Agg_yr=os.listdir(pi1)
    for j in Agg_yr:
        pj1=pi1+j+"/"
        Agg_yr_list=os.listdir(pj1)
        for k in Agg_yr_list:
            pk1=pj1+k
            Data1=open(pk1,'r')
            d1=json.load(Data1)
            for l1 in d1['data']['transactionData']:
                Name=l1['name']
                Trancount=l1['paymentInstruments'][0]['count']
                amount=l1['paymentInstruments'][0]['amount']
                clm1['Transacion_type'].append(Name)
                clm1['Transacion_count'].append(Trancount)
                clm1['Transacion_amount'].append(amount)
                clm1['State'].append(i)
                clm1['Year'].append(j)
                clm1['Quater'].append(int(k.strip('.json')))

Agg_Trans=pd.DataFrame(clm1)

Agg_Trans['State']=Agg_Trans['State'].str.replace("-"," ")
Agg_Trans['State']=Agg_Trans["State"].str.title()
Agg_Trans['State']=Agg_Trans["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Agg_Trans['State']=Agg_Trans['State'].str.replace("Andaman & Nicobar Islands","Andaman & Nicobar")

#Aggregated user details
path2="C:/Blast/PortableGit/pulse/data/aggregated/user/country/india/state/"
Agg_user_list=os.listdir(path2)

clm2={'State':[], 'Year':[],'Quater':[],'Brands':[],'Transactioncount':[],'Totalpercent':[]}

for i in Agg_user_list:
    pi2=path2+i+"/"
    Agg_yr=os.listdir(pi2)
    for j in Agg_yr:
        pj2=pi2+j+"/"
        Agg_yr_list=os.listdir(pj2)
        for k in Agg_yr_list:
            pk2=pj2+k
            Data2=open(pk2,'r')
            d2=json.load(Data2)
            #print(d2) there are none values so using try except.
            try:
                for l2 in d2['data']['usersByDevice']:
                    Brand=l2['brand']
                    Usercount=l2['count']
                    Percentage=l2['percentage']
                    clm2['Brands'].append(Brand)
                    clm2['Transactioncount'].append(Usercount)
                    clm2['Totalpercent'].append(Percentage)
                    clm2['State'].append(i)
                    clm2['Year'].append(j)
                    clm2['Quater'].append(int(k.strip('.json')))    
            except:
                pass
Agg_users=pd.DataFrame(clm2)
Agg_users['State']=Agg_users['State'].str.replace("-"," ")
Agg_users['State']=Agg_users["State"].str.title()
Agg_users['State']=Agg_users["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Agg_users['State']=Agg_users['State'].str.replace("Andaman & Nicobar Islands","Andaman & Nicobar")

#Map transsaction details
path3="C:/Blast/PortableGit/pulse/data/map/transaction/hover/country/india/state/"
Map_tran_list=os.listdir(path3)

clm3={'State':[], 'Year':[],'Quater':[],'Dist_Name':[],'Transaction_count':[],'TotalAmount':[]}

for i in Map_tran_list:
    pi3=path3+i+"/"
    Map_yr=os.listdir(pi3)
    for j in Map_yr:
        pj3=pi3+j+"/"
        Map_yr_list=os.listdir(pj3)
        for k in Map_yr_list:
            pk3=pj3+k
            Data3=open(pk3,'r')
            d3=json.load(Data3)
            
            for l3 in d3['data']['hoverDataList']:
                Name=l3['name']
                Count=l3['metric'][0]['count']
                Amount=l3['metric'][0]['amount']
                clm3['Dist_Name'].append(Name)
                clm3['Transaction_count'].append(Count)
                clm3['TotalAmount'].append(Amount)
                clm3['State'].append(i)
                clm3['Year'].append(j)
                clm3['Quater'].append((int(k.strip('.json'))))
            
Map_Trans=pd.DataFrame(clm3)
Map_Trans['State']=Map_Trans['State'].str.replace("-"," ")
Map_Trans['State']=Map_Trans["State"].str.title()
Map_Trans['State']=Map_Trans["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Map_Trans['State']=Map_Trans['State'].str.replace("Andaman & Nicobar Islands","Andaman & Nicobar")

#Map user details
path4="C:/Blast/PortableGit/pulse/data/map/user/hover/country/india/state/"
Map_user_list=os.listdir(path4)

clm4={'State':[], 'Year':[],'Quater':[],'Distusername':[],'Regi_users':[],'App_opens':[]}

for i in Map_user_list:
    pi4=path4+i+"/"
    Map_yr=os.listdir(pi4)
    for j in Map_yr:
        pj4=pi4+j+"/"
        Map_yr_list=os.listdir(pj4)
        for k in Map_yr_list:
            pk4=pj4+k
            Data4=open(pk4,'r')
            d4=json.load(Data4)
            
            for l4 in d4['data']['hoverData'].items():
                District=l4[0]
                RegisteredUsers=l4[1]['registeredUsers']
                AppOpens=l4[1]['appOpens']
                clm4["Distusername"].append(District)
                clm4["Regi_users"].append(RegisteredUsers)
                clm4['App_opens'].append(AppOpens)
                clm4['State'].append(i)
                clm4['Year'].append(j)
                clm4['Quater'].append((int(k.strip('.json'))))
            
Map_Users=pd.DataFrame(clm4)
Map_Users['State']=Map_Users['State'].str.replace("-"," ")
Map_Users['State']=Map_Users["State"].str.title()
Map_Users['State']=Map_Users["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Map_Users['State']=Map_Users['State'].str.replace("Andaman & Nicobar Islands","Andaman & Nicobar")

#top transaction details
path5="C:/Blast/PortableGit/pulse/data/top/transaction/country/india/state/"
top_trans_list=os.listdir(path5)

clmdist={'State':[], 'Year':[],'Quater':[],'TopDistname':[],'TopDistCount':[],'TopDistAmount':[]}
clmpin={'State':[], 'Year':[],'Quater':[],'TopPincode':[],'TopPinCount':[],'TopPinAmount':[]}
for i in top_trans_list:
    pi5=path5+i+"/"
    top_yr=os.listdir(pi5)
    for j in top_yr:
        pj5=pi5+j+"/"
        top_yr_list=os.listdir(pj5)
        for k in top_yr_list:
            pk5=pj5+k
            Data5=open(pk5,'r')
            d5=json.load(Data5)
            
            for l5 in d5['data']['districts']:
                name1=l5['entityName']
                count1=l5['metric']['count']
                amount1=l5['metric']['amount']
                clmdist['TopDistname'].append(name1)
                clmdist['TopDistCount'].append(count1)
                clmdist['TopDistAmount'].append(amount1)
                clmdist['State'].append(i)
                clmdist['Year'].append(j)
                clmdist['Quater'].append((int(k.strip('.json'))))

            for l9 in d5['data']['pincodes']:
                pincode=l9['entityName']
                count2=l9['metric']['count']
                amount2=l9['metric']['amount']
                clmpin['TopPincode'].append(pincode)
                clmpin['TopPinCount'].append(count2)
                clmpin['TopPinAmount'].append(amount2)
                clmpin['State'].append(i)
                clmpin['Year'].append(j)
                clmpin['Quater'].append((int(k.strip('.json'))))

Top_trans_dist=pd.DataFrame(clmdist)
Top_trans_dist['State']=Top_trans_dist['State'].str.replace("-"," ")
Top_trans_dist['State']=Top_trans_dist["State"].str.title()
Top_trans_dist['State']=Top_trans_dist["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Top_trans_dist['State']=Top_trans_dist['State'].str.replace("Andaman & Nicobar Islands","Andaman & Nicobar")

Top_trans_pin=pd.DataFrame(clmpin)
Top_trans_pin['State']=Top_trans_pin['State'].str.replace("-"," ")
Top_trans_pin['State']=Top_trans_pin["State"].str.title()
Top_trans_pin['State']=Top_trans_pin["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Top_trans_pin['State']=Top_trans_pin['State'].str.replace("Andaman & Nicobar Islands","Andaman & Nicobar")

#Top user details
path6="C:/Blast/PortableGit/pulse/data/top/user/country/india/state/"
top_user_list=os.listdir(path6)

clmudist={'State':[], 'Year':[],'Quater':[],'TopUserDistname':[],'TopDistRegUser':[]}
clmupin={'State':[], 'Year':[],'Quater':[],'TopUserPincode':[],'TopPinUsers':[]}
for i in top_user_list:
    pi6=path6+i+"/"
    top_user_yr=os.listdir(pi6)
    for j in top_user_yr:
        pj6=pi6+j+"/"
        top_useryr_list=os.listdir(pj6)
        for k in top_useryr_list:
            pk6=pj6+k
            Data6=open(pk6,'r')
            d6=json.load(Data6)

            for l7 in d6['data']['districts']:
                name3=l7['name']
                RegisteredUsers3=l7['registeredUsers']
                clmudist['TopUserDistname'].append(name3)
                clmudist['TopDistRegUser'].append(RegisteredUsers3)
                clmudist['State'].append(i)
                clmudist['Year'].append(j)
                clmudist['Quater'].append((int(k.strip(".json"))))

            for l8 in d6['data']['pincodes']:
                pincode4=l8['name']
                RegisteredUsers4=l8['registeredUsers']
                clmupin['TopUserPincode'].append(pincode4)
                clmupin['TopPinUsers'].append(RegisteredUsers4)
                clmupin['State'].append(i)
                clmupin['Year'].append(j)
                clmupin['Quater'].append((int(k.strip(".json"))))

Top_Users_dist=pd.DataFrame(clmudist)
Top_Users_dist['State']=Top_Users_dist['State'].str.replace("-"," ")
Top_Users_dist['State']=Top_Users_dist["State"].str.title()
Top_Users_dist['State']=Top_Users_dist["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Top_Users_dist['State']=Top_Users_dist['State'].str.replace("Andaman & Nicobar Islands","Andaman & Nicobar")

Top_Users_pin=pd.DataFrame(clmupin)
Top_Users_pin['State']=Top_Users_pin['State'].str.replace("-"," ")
Top_Users_pin['State']=Top_Users_pin["State"].str.title()
Top_Users_pin['State']=Top_Users_pin["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu")
Top_Users_pin['State']=Top_Users_pin['State'].str.replace("Andaman & Nicobar Islands","Andaman & Nicobar")




#Aggregated Transaction Table
mycursor.execute('''create table if not exists Agg_Transaction(State varchar(255),
                                                            Year int,
                                                            Quater int,
                                                            Transacion_type varchar(255),
                                                            Transacion_count int,
                                                            Transacion_amount int)''')

query1='''insert into Agg_Transaction (State,Year,Quater,Transacion_type,Transacion_count,
                                                            Transacion_amount) 
                                                            values(%s,%s,%s,%s,%s,%s)'''
SendData1=Agg_Trans.values.tolist()
for row1 in SendData1:
    mycursor.execute(query1,row1)
mydb.commit()
#agg_transaction to df
mycursor.execute("select * from agg_transaction")
mydb.commit()
A_T=mycursor.fetchall()
AggTraTable=pd.DataFrame(A_T,columns=("State","Year","Quater","AMTTYDS","Count","Amount"))



#Aggregated User Table
mycursor.execute('''create table if not exists Agg_Users(State varchar(255),
                                                            Year int,
                                                            Quater int,
                                                            Brands varchar(255),
                                                            Transacioncount int,
                                                            Totalpercent float)''')

query2='''insert into Agg_Users (State,Year,Quater,Brands,Transacioncount,
                                                            Totalpercent) 
                                                            values(%s,%s,%s,%s,%s,%s)'''
SendData2=Agg_users.values.tolist()
for row2 in SendData2:
    mycursor.execute(query2,row2)
mydb.commit()
#agg_user to df
mycursor.execute("select * from agg_users")
mydb.commit()
A_U=mycursor.fetchall()
AggUserTable=pd.DataFrame(A_U,columns=("State","Year","Quater","Brands","Transacioncount","Totalpercent"))



#Map Transaction Table
mycursor.execute('''create table if not exists Map_Transaction(State TEXT,
                                                            Year int,
                                                            Quater int,
                                                            Dist_Name TEXT,
                                                            Transaction_count int,
                                                            TotalAmount bigint)''')

query3='''insert into Map_Transaction (State,Year,Quater,Dist_Name,Transaction_count,TotalAmount) 
                                                            values(%s,%s,%s,%s,%s,%s)'''
SendData3=Map_Trans.values.tolist()
for row3 in SendData3:
    mycursor.execute(query3,row3)
mydb.commit()
#map_transaction to df
mycursor.execute("select * from map_transaction")
mydb.commit()
M_T=mycursor.fetchall()
MapTraTable=pd.DataFrame(M_T,columns=("State","Year","Quater","AMTTYDS","Count","Amount"))



#Map User Table
mycursor.execute('''create table if not exists Map_users(State varchar(255),
                                                            Year int,
                                                            Quater int,
                                                            Distusername varchar(255),
                                                            Regi_users bigint,
                                                            App_opens bigint)''')

query4='''insert into Map_users (State,Year,Quater,Distusername,Regi_users,
                                                            App_opens) 
                                                            values(%s,%s,%s,%s,%s,%s)'''
SendData4=Map_Users.values.tolist()
for row4 in SendData4:
    mycursor.execute(query4,row4)
mydb.commit()
#map_user to df
mycursor.execute("select * from map_users")
mydb.commit()
M_U=mycursor.fetchall()
MapUserTable=pd.DataFrame(M_U,columns=("State","Year","Quater","AMTTYDS","Count","Amount"))



#Top Transaction pin Table
mycursor.execute('''create table if not exists top_transaction_pin(State varchar(255),
                                                            Year int,
                                                            Quater int,
                                                            TopPincode varchar(255),
                                                            TopPinCount int,
                                                            TopPinAmount float)''')

queryp='''insert into top_transaction_pin(State,Year,Quater,TopPincode,TopPinCount,
                                        TopPinAmount) 
                                        values(%s,%s,%s,%s,%s,%s)'''
SendDatap=Top_trans_pin.values.tolist()
for rowp in SendDatap:
    mycursor.execute(queryp,rowp)
mydb.commit()
#top_transaction pin to df
mycursor.execute("select * from top_transaction_pin")
mydb.commit()
T_TP=mycursor.fetchall()
ToppinTable=pd.DataFrame(T_TP,columns=("State","Year","Quater","AMTTYDS","Count","Amount"))
ToppinTable["AMTTYDS"]=ToppinTable["AMTTYDS"].str.cat(['_']*len(ToppinTable), sep='')



#Top User Table
mycursor.execute('''create table if not exists TopUserspin(State varchar(255),
                                                            Year int,
                                                            Quater int,
                                                            TopUserPincode TEXT,
                                                            TopPinUsers int)''')

queryup='''insert into TopUserspin (State,Year,Quater,TopUserPincode,TopPinUsers) 
                                        values(%s,%s,%s,%s,%s)'''
SendDataup=Top_Users_pin.values.tolist()
for rowup in SendDataup:
    mycursor.execute(queryup,rowup)
mydb.commit()
#top_users to df
mycursor.execute("select * from topuserspin")
mydb.commit()
T_Up=mycursor.fetchall()
TopUserpinTable=pd.DataFrame(T_Up,columns=("State","Year","Quater","TopUserPincode","TopPinUsers"))
TopUserpinTable["TopUserPincode"]=TopUserpinTable["TopUserPincode"].str.cat(['_']*len(TopUserpinTable), sep='')




#Transaction Analaysis
#transaction Analaysis by year
def trans_year(df,year):
    MT=df[df["Year"]==year]
    MT.reset_index(drop=True,inplace=True)

    MTg=MT.groupby("State")[["Count","Amount"]].sum()
    MTg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.choropleth(
                    MTg,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Amount',
                    hover_name="State",
                    color_continuous_scale="purples",
                    title=f"Transaction Amount for {year}",
                    width=550
                )
        fig_amount.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_amount)
        

    with col2:
        fig_count = px.choropleth(
                    MTg,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Count',
                    hover_name="State",
                    color_continuous_scale="purples",
                    title=f"Transaction Count for {year}",
                    width=550
                )
        fig_count.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_count)
        

    return MT

#transaction analaysis by quater
def trans_y_q(df,quater):
    MTYQ=df[df["Quater"]==quater]
    MTYQ.reset_index(drop=True,inplace=True)

    MTQg=MTYQ.groupby("State")[["Count","Amount"]].sum()
    MTQg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.choropleth(
                        MTQg,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Amount',
                        hover_name="State",
                        color_continuous_scale="purples",
                        title=f"Transaction Amount for Quater {quater}",
                        width=550
                    )
        fig_amount.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_amount)
        

    with col2:
        fig_count = px.choropleth(
                        MTQg,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Count',
                        hover_name="State",
                        color_continuous_scale="purples",
                        title=f"Transaction Count for Quater {quater}",
                        width=550
                    )
        fig_count.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_count)
        
    return MTYQ

#transaction analysis by State
def transstate(df,state):
    mts=df[df["State"]==state]
    mts.reset_index(drop=True,inplace=True)

    mtsg=mts.groupby("AMTTYDS")[["Count","Amount"]].sum()
    mtsg.reset_index(inplace=True)

    fig_bar_1=px.bar(mtsg,x="AMTTYDS",y="Amount",title=f"Transaction Total Amount in {state} of Q={mts["Quater"].min()} Y={mts["Year"].min()}",
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_name="AMTTYDS")
    st.plotly_chart(fig_bar_1)
    
    fig_bar_2=px.bar(mtsg,x="AMTTYDS",y="Count",title=f"Transaction Count in {state} of Q={mts["Quater"].min()} Y={mts["Year"].min()}",
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_name="AMTTYDS")
    st.plotly_chart(fig_bar_2)
    
#Aggregated user analaysis 1 by years
def Aggre_user_plot_1(df,year):
    aguy=df[df["Year"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transacioncount"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands",y="Transacioncount",title=f"BRANDS AND THEIR TRANSACTION COUNT FOR {year}",
                    width=1000,color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Totalpercent"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_2=px.bar(aguyg,x="Brands",y="Totalpercent",title=f"BRANDS AND THEIR TRANSACTION PERCENT FOR {year}",
                    width=1000,color_discrete_sequence=px.colors.sequential.Agsunset)
    st.plotly_chart(fig_bar_2)
    return aguy

#Aggregated user analaysis 2 by quaters
def Aggre_user_plot_2(df,quater) :
    aguyq=df[df["Quater"]==quater]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transacioncount"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg,x="Brands",y="Transacioncount",title=f"BRANDS AND THEIR TRANSACTION COUNT FOR QUATER {quater} OF {aguyq["Year"].min()}",
                        width=1000,color_discrete_sequence=px.colors.sequential.Agsunset)
    st.plotly_chart(fig_bar_1)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Totalpercent"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_2=px.bar(aguyqg,x="Brands",y="Totalpercent",title=f"BRANDS AND THEIR TRANSACTION PERCENT FOR QUATER {quater} OF {aguyq["Year"].min()}",
                        width=1000,color_discrete_sequence=px.colors.sequential.Agsunset)
    st.plotly_chart(fig_bar_2)
    return aguyq

#Aggregated user analaysis 3 by states
def Aggregated_user_plot_3(df,state):
    aguyqs=df[df["State"]==state]
    aguyqs.reset_index(drop=True,inplace=True)

    aguyqsg=pd.DataFrame(aguyqs.groupby("Brands")[["Transacioncount","Totalpercent"]].sum())
    aguyqsg.reset_index(inplace=True)
    fig_line_1=px.line(aguyqsg,x="Brands",y="Transacioncount",hover_data="Totalpercent",hover_name="Brands",
                    title=f"BRANDS AND THEIR TRANSACTION COUNT & PERCENT OF {state.upper()} Q={aguyqs["Quater"].min()} Y={aguyqs["Year"].min()}",
                    markers=True)
    st.plotly_chart(fig_line_1)

#top user plot
def topuserdetail(df,year):
    tuy=df[df["Year"]==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["State","Quater"])["TopPinUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_1=px.bar(tuyg,x="State",y="TopPinUsers",color="Quater",
                    color_discrete_sequence=px.colors.sequential.Agsunset,height=700,
                    hover_name="State",title=f"{year} Registered Users")
    st.plotly_chart(fig_top_1)
    return tuy

def topuserq(df,quater):
    tuys=df[df["Quater"]==quater]
    tuys.reset_index(drop=True, inplace=True)
    tuysg=pd.DataFrame(tuys.groupby("State")["TopPinUsers"].sum())
    tuysg.reset_index(inplace=True)
    fig=px.bar(tuys,x="State",y="TopPinUsers",title=f"{quater}st Quater Details",height=700)
    st.plotly_chart(fig)
    return tuys

def topuserstate(df,state):
    tuyqs=df[df["State"]==state]
    tuyqs.reset_index(drop=True, inplace=True)
    tuyqsg=pd.DataFrame(tuyqs.groupby("TopUserPincode")["TopPinUsers"].sum())
    tuyqsg.reset_index(inplace=True)
    fig=px.bar(tuyqsg,x="TopUserPincode",y="TopPinUsers",title=f"{state} Details")
    st.plotly_chart(fig)

def top_chart_transamt(table_name,column_name,c):
    #connection to database
    mydb = mysql.connector.connect(host="localhost",user="root",password="",)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("use newphonepe")
    #plot1
    query1=f'''select state,sum({column_name}) from {table_name}
                group by state
                order by sum({column_name}) desc
                limit 10'''
    mycursor.execute(query1)
    table1=mycursor.fetchall()
    mydb.commit()
    df1=pd.DataFrame(table1,columns=("States",f"{c}"))
    col1,col2=st.columns(2)
    with col1:
        figbar1=px.bar(df1,x="States",y=f"{c}",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,
                    hover_name="States",title="Top 10")
        st.plotly_chart(figbar1)

    #plot2
    query2=f'''select state,sum({column_name}) from {table_name}
                group by state
                order by sum({column_name}) asc
                limit 10'''
    mycursor.execute(query2)
    table2=mycursor.fetchall()
    mydb.commit()
    df2=pd.DataFrame(table2,columns=("States",f"{c}"))
    with col2:
        figbar2=px.bar(df2,x="States",y=f"{c}",color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=600,
                    hover_name="States",title="Least 10")
        st.plotly_chart(figbar2)

    #plot3
    query3=f'''select state,avg({column_name}) from {table_name}
                group by state
                order by avg({column_name})'''
    mycursor.execute(query3)
    table3=mycursor.fetchall()
    mydb.commit()
    df3=pd.DataFrame(table3,columns=("States",f"{c}"))
    figbar3=px.bar(df3,y="States",x=f"{c}",color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,
                orientation="h",hover_name="States",title="Average Transaction")
    st.plotly_chart(figbar3)

def format_number(number):
    s,*d= str(number).partition(".")
    result = ",".join([s[x - 2 : x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return result

def mcrores(number):
    return '₹'+'{:,.0f} Cr'.format(round(number / 10000000))

def trause(a,b,c,d):
    map_df = a.loc[(a['Quater']==int(c)) & (a['Year']==int(b))]
    map_df1 = map_df.groupby('State').agg({'Count':'sum','Amount':'sum'}).reset_index()
    fst = map_df1.copy()
    fst['All Transactions'] = fst['Count'].apply(lambda x: round(x)).apply(lambda x: format_number(x))
    fst['Total Payment Values'] = fst['Amount'].apply(lambda x: round(x)).apply(lambda x: mcrores(x))
    fst['Avg.Transaction Value'] = fst['Amount'] / fst['Count']
    fst['Avg.Transaction Value'] = fst['Avg.Transaction Value'].apply(lambda x: round(x)).apply(lambda x: "₹{:,.0f}".format(x))
    fig1 = px.choropleth_mapbox(
        fst,
        locations="State",
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        color="Count",
        featureidkey='properties.ST_NM',
        hover_name="State",
        hover_data={'All Transactions':True,'Total Payment Values':True,'State':False,'Avg.Transaction Value':True,'Count':False},
        title=f"PhonePe {d} in Q {b}-{c}",
        mapbox_style="carto-positron",
        center={"lat": 24, "lon": 79},
        color_continuous_scale=px.colors.sequential.Aggrnyl,
        zoom=3.6,
        #width=800, 
        height=800
    )
    fig1.update_layout(coloraxis_colorbar=dict(title=' ', showticklabels=True),title={'font': {'size': 24}},
                    hoverlabel_font={'size': 14})
    st.plotly_chart(fig1)

def sdp(df):
    csdf=pd.DataFrame(df,columns=("Distrcts","Total"))
    csdf["Distrcts"]=csdf["Distrcts"].str.title()
    csdf1=csdf["Total"].apply(lambda x: mcrores(x))
    csdf["Total"]=csdf1
    cf1,cf2,cf3=st.columns(3)
    with cf1:
        dd1=csdf["Distrcts"][0]
        st.markdown(f'#### :orange[1.] {dd1}')
        st.write('')
        dd2=csdf["Distrcts"][1]
        st.write(f'#### :orange[2.] {dd2}')
        st.write('')
        dd3=csdf["Distrcts"][2]
        st.write(f'#### :orange[3.] {dd3}')
        st.write('')
        dd4=csdf["Distrcts"][3]
        st.write(f'#### :orange[4.] {dd4}')
        st.write('')
        dd5=csdf["Distrcts"][4]
        st.write(f'#### :orange[5.] {dd5}')
        st.write('')
        dd6=csdf["Distrcts"][5]
        st.write(f'#### :orange[6.] {dd6}')
        st.write('')
        dd7=csdf["Distrcts"][6]
        st.write(f'#### :orange[7.] {dd7}')
        st.write('')
        dd8=csdf["Distrcts"][7]
        st.write(f'#### :orange[8.] {dd8}')
        st.write('')
        dd9=csdf["Distrcts"][8]
        st.write(f'#### :orange[9.] {dd9}')
        st.write('')
        dd10=csdf["Distrcts"][9]
        st.write(f'#### :orange[10.] {dd10}')
        st.write('')
    with cf2:
        vv1=csdf["Total"][0]
        st.write(f'#### :violet[{vv1}]')
        st.write('')
        vv2=csdf["Total"][1]
        st.write(f'#### :violet[{vv2}]')
        st.write('')
        vv3=csdf["Total"][2]
        st.write(f'#### :violet[{vv3}]')
        st.write('')
        vv4=csdf["Total"][3]
        st.write(f'#### :violet[{vv4}]')
        st.write('')
        vv5=csdf["Total"][4]
        st.write(f'#### :violet[{vv5}]')
        st.write('')
        vv6=csdf["Total"][5]
        st.write(f'#### :violet[{vv6}]')
        st.write('')
        vv7=csdf["Total"][6]
        st.write(f'#### :violet[{vv7}]')
        st.write('')
        vv8=csdf["Total"][7]
        st.write(f'#### :violet[{vv8}]')
        st.write('')
        vv9=csdf["Total"][8]
        st.write(f'#### :violet[{vv9}]')
        st.write('')
        vv10=csdf["Total"][9]
        st.write(f'#### :violet[{vv10}]')
        st.write('')

#streamlit continue
if select=="Explore Data":
    tab1,tab2,tab3=st.tabs(["Aggregated","Map Analysis","Top Analysis"])

    with tab1:
        m1=st.radio("Select to Analyse ",["AggTransaction","AggUsers"])
        if m1=="AggTransaction":
            col1,col2,col3,col4=st.columns(4)
            with col1:
                years=st.selectbox("Select the Year",AggTraTable["Year"].unique())
            atyq=trans_year(AggTraTable,years)

            col1,col2,col3=st.columns(3)
            with col1:
                quarters=st.selectbox("Select the Quater",atyq["Quater"].unique())
            atyqs=trans_y_q(atyq,quarters)

            col1,col2,col3=st.columns(3)
            with col1:
                States=st.selectbox("Select the State",atyq["State"].unique())
            transstate(atyqs,States)

        elif m1=="AggUsers":
            col1,col2,col3,col4=st.columns(4)
            with col1:
                AUyears=st.selectbox("Year",AggUserTable["Year"].unique())
            Aggre_user_Y=Aggre_user_plot_1(AggUserTable,AUyears)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                AUquater=st.selectbox("Quater",Aggre_user_Y["Quater"].unique())
            Aggre_user_y_q=Aggre_user_plot_2(Aggre_user_Y,AUquater)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                AUstate=st.selectbox("State",Aggre_user_y_q["State"].unique())
            Aggre_user_y_q_s=Aggregated_user_plot_3(Aggre_user_y_q,AUstate)
        else:
            pass

    with tab2:
        m2=st.radio("Select to Analyse ",["MapTransaction","MapUsers"])
        if m2=="MapTransaction":
            col1,col2,col3,col4=st.columns(4)
            with col1:
                Mtyears=st.selectbox("Select by Year",MapTraTable["Year"].unique())
            Mapbyyear=trans_year(MapTraTable,Mtyears)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                MTquaters=st.selectbox("Select by Quater",Mapbyyear["Quater"].unique())
            Mapbyquater=trans_y_q(Mapbyyear,MTquaters)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                mtstate=st.selectbox("Select by State",Mapbyquater["State"].unique())
            transstate(Mapbyquater,mtstate)

        elif m2=="MapUsers":
            st.header("Amount = AppOpens & Count = Registered Users")
            col1,col2,col3,col4=st.columns(4)
            with col1:
                Muyears=st.selectbox("By Year",MapUserTable["Year"].unique())
            st.markdown("Amount = AppOpens & Count = Registered Users")
            Mapubyyear=trans_year(MapUserTable,Muyears)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                Muquaters=st.selectbox("By Quater",Mapubyyear["Quater"].unique())
            st.markdown("Amount = AppOpens & Count = Registered Users")
            Mapubyquater=trans_y_q(Mapubyyear,Muquaters)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                mustate=st.selectbox("By State",Mapubyquater["State"].unique())
            st.markdown("Amount = AppOpens & Count = Registered Users")
            transstate(Mapubyquater,mustate)
        else:
            pass

    with tab3:
        m3=st.radio("Select to Analyse ",["TopTransaction by District","TopUsers by District","TopTransaction by Pincode","TopUsers by Pincode"])
        if m3=="TopTransaction by District":
            st.header("Please Refer to MapTransaction Details")
            st.markdown("Thank You")
        elif m3=="TopUsers by District":
            st.header("Please refer Map User Details for TopUsers by District")
            st.markdown("Thank You...")
        elif m3=="TopTransaction by Pincode":
            col1,col2,col3,col4=st.columns(4)
            with col1:
                ttpy=st.selectbox("In Year",ToppinTable["Year"].unique())
            ttbypin=trans_year(ToppinTable,ttpy)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                ttpq=st.selectbox("In Quater",ttbypin["Quater"].unique())
            ttqbypin=trans_y_q(ttbypin,ttpq)

            col1,col2,col3,col4=st.columns(4)
            with col1:
                ttpqb=st.selectbox("In State",ttqbypin["State"].unique())
            transstate(ttqbypin,ttpqb)

        elif m3=="TopUsers by Pincode":
            col1,col2=st.columns(2)
            with col1:
                tupy=st.select_slider("Which Year",TopUserpinTable["Year"].unique())
            tupyq=topuserdetail(TopUserpinTable,tupy)

            col1,col2=st.columns(2)
            with col1:
                tupq=st.select_slider("Which Quater",tupyq["Quater"].unique())
            tupyqs=topuserq(tupyq,tupq)

            col1,col2=st.columns(2)
            with col1:
                tus=st.selectbox("which State",tupyqs["State"].unique())
            topuserstate(tupyqs,tus)
        else:
            pass

elif select=="Insights":
    ta1,ta2,ta3,ta4,ta5,ta6=st.tabs(["Top Charts","All India","Categories","States","Districts","Postal Codes"])
    with ta1:
        st.title(":rainbow[Top Charts]")
        charts=st.selectbox("",["1.Transaction Amount and Count of Aggregated Transaction",
                                        "2.Transaction Amount and Count of Map Transaction",
                                        "3.Transaction Amount and Count of Top Pincode Transaction",
                                        "4.Transaction Count of Aggregated Users",
                                        "5.Registered Users and App opens of Map Users",
                                        "6.Registered Users for available Pincode"]) 
        if charts=="1.Transaction Amount and Count of Aggregated Transaction":
            tab1,tab2=st.tabs(["Transaction Amount","Transaction Count"])
            with tab1:
                top_chart_transamt("agg_transaction","transacion_amount","Transaction Amount")
            with tab2:
                top_chart_transamt("agg_transaction","transacion_count","Transaction Count")

        if charts=="2.Transaction Amount and Count of Map Transaction":
            tab1,tab2=st.tabs(["Transaction Amount","Transaction Count"])
            with tab1:
                top_chart_transamt("map_transaction","totalamount","Transaction Amount")
            with tab2:
                top_chart_transamt("map_transaction","Transaction_count","Transaction Count")

        if charts=="3.Transaction Amount and Count of Top Pincode Transaction":
            tab1,tab2=st.tabs(["Transaction Amount","Transaction Count"])
            with tab1:
                top_chart_transamt("top_transaction_pin","toppinamount","Transaction Amount")
            with tab2:
                top_chart_transamt("top_transaction_pin","Toppincount","Transaction Count")

        if charts=="4.Transaction Count of Aggregated Users":
            top_chart_transamt("agg_users","transacioncount","UserCount")
        
        if charts=="5.Registered Users and App opens of Map Users":
            tab1,tab2=st.tabs(["Registered Users","App Opens"])
            with tab1:
                top_chart_transamt("map_users","regi_users","Registered Users")
            with tab2:
                top_chart_transamt("map_users","app_opens","App Opens")
        
        if charts=="6.Registered Users for available Pincode":
            top_chart_transamt("topuserspin","toppinusers","Pincode Users")

    with ta2:
        ha1,ha2=st.tabs(["Transactions","Users"])

        #Transactions
        with ha1:
            t1,c1,c2,c4=st.columns([8,2,2,2])
            with t1:
                st.title(":rainbow[Transactions]")
            with c1:
                yr1=st.selectbox('Year',MapTraTable["Year"].unique())
            with c2:
                quat1=st.selectbox('Quater',MapTraTable["Quater"].unique())

            ### Transaction values
            tr = MapTraTable.copy()
            filter_tr = tr.loc[(tr['Year']==int(yr1)) & (tr['Quater']==int(quat1))]
            gr_tr = filter_tr.groupby('Year').sum()
            All_transactions = gr_tr['Count'].to_list()[0]
            Total_payments =gr_tr['Amount'] 
            Total_payments1 =gr_tr['Amount'].to_list()[0]

            atl = format_number(All_transactions)

            Avg_Transaction = round(Total_payments1/All_transactions)
            av_form = '₹{:,}'.format(Avg_Transaction)

            sf1 = Total_payments.apply(lambda x: "₹" + "{:,.0f}".format(x/10000000) + "Cr")
            trvalue1 = sf1.to_list()[0] # ***Total payments

            st.write('## All Transactions (UPI+Cards+Wallets)')
            st.write(f'## :green[{atl}]')
            st.write('')

            ff1,ff2=st.columns(2)
            with ff1:
                st.write('### Total Payment Value')
                st.write(f'### :green[{trvalue1}]')

            with ff2:
                st.write('### Avg.Transaction Value')
                st.write(f'### :green[{av_form}]')
            trause(MapTraTable,yr1,quat1,"Amount Transactions")

        #Users    
        with ha2:
            na1,y1,qr1,em1=st.columns([8,2,2,2])
            with na1:
                st.title(":rainbow[Users]")
            with y1:
                yr2=st.selectbox('Years',MapUserTable["Year"].unique())
            with qr1:
                quat2=st.selectbox('Quaters',MapUserTable["Quater"].unique())
            ur = MapUserTable.copy()

            filter_ur = ur.loc[(ur['Year']==int(yr2)) & (ur['Quater']==int(quat2))]
            gr_ur = filter_ur.groupby('Year').sum()
            Registered_users = gr_ur['Count'].to_list()[0] #****Registered users****
            reg_usr = format_number(Registered_users)
            App_opens = int(gr_ur['Amount'].to_list()[0]) #****App opens****
            app_on = format_number(App_opens)
            
            thn1,thn2=st.columns(2)
            with thn1:
                st.write(f'### Registered PhonePe users till Q{quat2} {yr2}')
                st.write(f'## :green[{reg_usr}]')
            with thn2:
                st.write(f'### PhonePe app opens in Q{quat2} {yr2}')
                st.write(f'## :green[{app_on}]')
            
            st.write('##### :blue[All Transactions    = Registered Users]')
            st.write('##### :blue[Total Payment Value = App Opens]')
            trause(MapUserTable,yr2,quat2,"Registered Users")

    with ta3:
        na2,y2,qr2,em2=st.columns([8,2,2,2])
        with na2:
            st.title(":rainbow[Categories]")
        with y2:
            yr3=st.selectbox("",AggTraTable["Year"].unique())
        with qr2:
            quat3=st.selectbox("",AggTraTable["Quater"].unique())
        query=f'''SELECT transacion_type,sum(transacion_amount) from agg_transaction where year={yr3} and quater={quat3}
                    group by Transacion_type ORDER by sum(Transacion_amount) DESC'''
        mycursor.execute(query)
        tt=mycursor.fetchall()
        mydb.commit()
        th=pd.DataFrame(tt,columns=("Categories","Transaction"))
        th1=th["Transaction"].apply(lambda x: format_number(x))
        fc1,fc2=st.columns(2)
        with fc1:
            peer=th["Categories"][0]
            st.write(f'#### :green[{peer}]')
            st.write('')
            mrch=th["Categories"][1]
            st.write(f'#### :blue[{mrch}]')
            st.write('')
            rb=th["Categories"][2]
            st.write(f'#### :gray[{rb}]')
            st.write('')
            other=th["Categories"][3]
            st.write(f'#### :orange[{other}]')
            st.write('')
            fin=th["Categories"][4]
            st.write(f'#### :red[{fin}]')
            st.write('')
        
        with fc2:
            val1=th1[0]
            st.write(f'#### :violet[{val1}]')
            st.write('')
            val2=th1[1]
            st.write(f'#### :violet[{val2}]')
            st.write('')
            val3=th1[2]
            st.write(f'#### :violet[{val3}]')
            st.write('')
            val4=th1[3]
            st.write(f'#### :violet[{val4}]')
            st.write('')
            val5=th1[4]
            st.write(f'#### :violet[{val5}]')
            st.write('')
        fg=px.pie(th,values="Transaction",names="Categories",color_discrete_sequence=px.colors.sequential.Aggrnyl,
                  hole=0.5)
        st.plotly_chart(fg)

    with ta5:
        na3,y3,qr3,em3=st.columns([8,2,2,2])
        with na3:
            st.title(":rainbow[Top 10 Districts]")
        with y3:
            yr5=st.selectbox('Y',MapTraTable["Year"].unique())
        with qr3:
            quat5=st.selectbox('Q',MapTraTable["Quater"].unique())
        cory=f'''SELECT Dist_Name,sum(TotalAmount) FROM `map_transaction`where Year={yr5} and Quater={quat5}
        group by Dist_Name ORDER by sum(TotalAmount) DESC limit 10 '''
        mycursor.execute(cory)
        cy=mycursor.fetchall()
        mydb.commit()
        sdp(cy)

    with ta4:
        na4,y4,qr4,em4=st.columns([8,2,2,2])
        with na4:
            st.title(":rainbow[Top 10 States]")
        with y4:
            yr6=st.selectbox('Yr',AggTraTable["Year"].unique())
        with qr4:
            quat6=st.selectbox('Qtr',AggTraTable["Quater"].unique())
        coryy=f'''SELECT state,sum(Transacion_amount) FROM `agg_transaction` WHERE Year={yr6} and Quater={quat6}
                    GROUP by State ORDER by sum(Transacion_amount) DESC LIMIT 10 '''
        mycursor.execute(coryy)
        cs=mycursor.fetchall()
        mydb.commit()
        sdp(cs)

    with ta6:
        na6,y6,qr6,em6=st.columns([8,2,2,2])
        with na6:
            st.title(":rainbow[Top 10 Postal Codes]")
        with y6:
            yr7=st.selectbox('Yrs',ToppinTable["Year"].unique())
        with qr6:
            quat7=st.selectbox('Quatr',ToppinTable["Quater"].unique())
        corryy=f'''SELECT Toppincode,sum(TopPinAmount) FROM `top_transaction_pin` WHERE year={yr7} and Quater={quat7}
                    group by TopPincode ORDER by sum(TopPinAmount) DESC LIMIT 10'''
        mycursor.execute(corryy)
        cp=mycursor.fetchall()
        mydb.commit()
        sdp(cp)

elif select=="KeyPoints":
    st.title(":rainbow[Key Points/Insights]")
    st.markdown("#### :orange[Point 5 Conclusion]")
    st.markdown("### :violet[Point 1]")
    st.write('''By analysing the below plot we can see there is a drastic increase in transaction happened,transaction count,
                Registeredusers and usage of the app.''')
    mycursor.execute('''SELECT Year,sum(transacion_amount) FROM `agg_transaction` GROUP by Year''')
    xx=mycursor.fetchall()
    dfxx=pd.DataFrame(xx,columns=("Year","Total"))
    line_1=px.line(dfxx,x="Year",y="Total",
                    title="Years 2018 to 2023",
                    markers=True)
    st.plotly_chart(line_1)
    st.write('')
    st.markdown("### :violet[Point 2]")
    st.caption("So for the available data from 2018 to 2023 the Reasons for this development could be")
    st.write("1. During these period almost all parts of the country people started using Internet...")
    st.write("2. Eveybody started using smartphones in digital india...")
    st.write("3. UPI transaction become very convenient , no need to carry cash all the time because nook and corner everybody using upi...")
    st.write("4. Due to Covid-19 ,as there is risk of infections handling cash,using upi for all type of payments become inevitable...")
    st.write("5. As PhonePe is india's leading UPI service and Public liked and using it for their covenience...")
    st.write('')
    st.markdown("### :violet[Point 3]")
    st.caption("Leading States/Districts/Cities...")
    st.write("1. During this period we can see states like Maharastra,Karnataka,Andhra and Telangana leading...")
    st.write("2. Reasons could be well educated peoples in cities like Banglore(Tech Gaint of India),Mumbai and Hydrabad(countries economy contributers)")
    st.write("3. Lot of IT industries,best available networks,more people living")
    st.write("4. Comparitively higher population")
    st.write("5. Small Info can create bigger impact")
    st.write('')
    st.markdown("### :violet[Point 4]")
    st.caption("Least Usage States/Districts/Cities...")
    st.write("1. Some North east and North and Islands of India are staying in the bottom of the records")
    st.write("2. Comparitively slow developing areas,less educated due to so may reasons")
    st.write("3. Restrictions and high alert areas")
    st.write("4. Comparitively lower populations")
    st.write("5. Less (Rich people,business,industries) and Internet Facilities(Infrastructures),following old fashions")
    st.write("")
    st.markdown("### :rainbow[Point 5 Conclusion]")
    st.caption("So how phonepe can be leading and Growth More")
    st.write('''**India is a Developing countries,in fully transforming into digital india UPI is going to be an important role ,
            Phonepe can keep up the good work and continue to evolve they can do ...**''')
    col1,col2=st.columns([2,5])
    with col2:
        st.write("* More Advertise ")
        st.write("* More word of mouth Propagation")
        st.write("* Bringing more Versetility to their Services")
        st.write("* Gaining more Trust,try to make place in peoples heart")
        st.write("* Comparitively give more compliments than others competitors")
        st.write("* Improve support system and easy Asses")
        st.write("* Making efforts to gain attention and popularity in least effective areas.")
        st.write("* Etc.....")


    st.title(":green[To be Continued............]")
