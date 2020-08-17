import matplotlib.pyplot as plt
import paho.mqtt.client as paho
from threading import Thread
from tkinter import ttk
import tkinter as tk
import threading
import socket
import json
import ssl
import time
import datetime

global connflag,GUIflag,model_plot,heat_list
connflag = False
GUIflag = False
model_plot = {}
heat_list = []
for i in range(10):
    heat_list.append(0)

def temp():
    return 0

def report():
    return 0
def start_button():
    console_list.insert(0, "雲端分析功能 已開啟")
    TOPIC_Value = json.dumps({"startflag":"a"})
    mqttc.publish("EdgeComputingForAbnormalDetection/Subscribe",TOPIC_Value, qos=1)

def end_button():
    console_list.insert(0, "上傳數據已終止")
    TOPIC_Value = json.dumps({"startflag":"b"})
    mqttc.publish("EdgeComputingForAbnormalDetection/Subscribe",TOPIC_Value, qos=1)

def abnormal_button():
    return 0

def release():
    global report_plot,report_plot_zone
    report_lab["text"] = "     [無]"
    report_lab1["text"] = "     [無]"
    TOPIC_Value = json.dumps({"startflag":"c"})
    mqttc.publish("EdgeComputingForAbnormalDetection/Subscribe",TOPIC_Value, qos=1)
    report_plot = tk.PhotoImage(file = "abn_null.png")
    report_plot_zone["image"] = report_plot
    return 0

def GUI():
    global GUIflag,console_list,console_list1,console_list2,vendor_label,device_label,cert_label,cycle_label,peremeter_label
    global lambda_runtime_plot,device1_Data,memory_label,lambda_table,device1_name,device2_name,device3_name,device4_name,lambda_runtime
    global bm,device1_Data,report_lab,report_lab1,report_plot,report_plot_zone
    window = tk.Tk()
    window.title('異質檢測之邊緣運算解決方案')
    window.geometry("1280x960")
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 1), width=15, height=1).grid(row=0,column=0)
    tk.Label(window, text="廠商代號：", fg = "black", font=('DFKai-SB', 26), width=15, height=1,anchor = 'e').grid(row=1,column=0)
    vendor_label = tk.Label(window, text="", fg = "dimgray", font=('Arial', 22), width=13, height=1,relief="groove",borderwidth=3,anchor = 'w')
    vendor_label.grid(row=1,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 1), width=17, height=1).grid(row=2,column=0)
    tk.Label(window, text="設備名稱：", fg = "black", font=('DFKai-SB', 26), width=15, height=1,anchor = 'e').grid(row=3,column=0)
    device_label = tk.Label(window, text="", fg = "dimgray", font=('Arial', 22), width=13, height=1,relief="groove",borderwidth=3,anchor = 'w')
    device_label.grid(row=3,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 1), width=17, height=1).grid(row=4,column=1)
    tk.Label(window, text="憑證編號：", fg = "black", font=('DFKai-SB', 26), width=15, height=1,anchor = 'e').grid(row=5,column=0)
    cert_label = tk.Label(window, text="", fg = "dimgray", font=('Arial', 22), width=13, height=1,relief="groove",borderwidth=3,anchor = 'w')
    cert_label.grid(row=5,column=1)
    tk.Label(window, text="", fg = "black", font=('Microsoft JhengHei', 1), width=15, height=1).grid(row=6,column=0)
    tk.Label(window, text="記憶體使用量：", fg = "black", font=('DFKai-SB', 26), width=15, height=1,anchor = 'e').grid(row=7,column=0)
    memory_label = tk.Label(window, text="", fg = "black", font=('Arial', 22), width=13, height=1,relief="groove",borderwidth=3,anchor = 'w')
    memory_label.grid(row=7,column=1)
    tk.Label(window, text=" ", fg = "black", font=('DFKai-SB', 12), width=15, height=1).grid(row=8,column=0)
    tk.Label(window, text="系統週期：", fg = "black", font=('DFKai-SB', 26), width=15, height=1,anchor = 'e').grid(row=9,column=0)
    cycle_label = tk.Label(window, text="", fg = "black", font=('Arial', 22), width=13, height=1,relief="groove",borderwidth=3,anchor = 'w')
    cycle_label.grid(row=9,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 14), width=15, height=1).grid(row=10,column=0)
    tk.Label(window, text="採集頻率：", fg = "black", font=('DFKai-SB', 26), width=15, height=1,anchor = 'e').grid(row=11,column=0)
    peremeter_label = tk.Label(window, text="", fg = "black", font=('Arial', 22), width=13, height=1,relief="groove",borderwidth=3,anchor = 'w')
    peremeter_label.grid(row=11,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB',16), width=15, height=2).grid(row=12,column=0)
    lambda_label = tk.LabelFrame(window,width=50, height=10, text='雲端運算效能模型', font=('Microsoft JhengHei', 21),padx=8)
    lambda_label.grid(row=13,column=0,columnspan=2,rowspan=5)
    lambda_runtime = tk.PhotoImage(file = 'lambda_runtime_null.png')
    lambda_runtime_plot = tk.Label(lambda_label,image = lambda_runtime,relief="sunken",borderwidth=3,compound="right")#, width=210, height=200
    lambda_runtime_plot.grid(row=0,column=0)
    lambda_table = ttk.Treeview(lambda_label)
    tk.Label(lambda_label, text="", fg = "black", font=('Microsoft JhengHei', 1), width=5, height=1).grid(row=0,column=1)
    lambda_table.grid(row=0,column=2)
    lambda_table['show']="headings"
    lambda_table['columns'] = ['Stamp','Batch','RealTime']
    lambda_table.column('Stamp',width=105)
    lambda_table.column('Batch',width=70)
    lambda_table.column('RealTime',width=70)
    lambda_table.heading('Stamp',text='Stamp')
    lambda_table.heading('Batch',text='批量')
    lambda_table.heading('RealTime',text='耗時')
    tk.Label(window, text="", fg = "black", font=('Arial', 18), width=1, height=1).grid(row=1,column=2)
    
    console_label = tk.LabelFrame(window,width=70, height=13, text='動態分析報告', font=('Microsoft JhengHei', 21))
    console_label.grid(row=1,column=3,rowspan=7,columnspan = 4)
    
    lambda_label = tk.Label(console_label,width=14, height=1, text='系統狀態', font=('Microsoft JhengHei', 16))
    lambda_label.grid(row=0,column=2)
    console_list = tk.Listbox(console_label,width=21, height=8, font=('Microsoft JhengHei', 14), fg = "blue")
    console_list.grid(row=1,column=2)
    lambda_label = tk.Label(console_label,width=19, height=1, text='發佈端', font=('Microsoft JhengHei', 16))
    lambda_label.grid(row=0,column=0)
    console_list1 = tk.Listbox(console_label,width=26, height=8, font=('Microsoft JhengHei', 14), fg = "blue")
    console_list1.grid(row=1,column=0)
    lambda_label = tk.Label(console_label,width=31, height=1, text='接收端', font=('Microsoft JhengHei', 16))
    lambda_label.grid(row=0,column=1)
    console_list2 = tk.Listbox(console_label,width=42, height=8, font=('Microsoft JhengHei', 14), fg = "blue")
    console_list2.grid(row=1,column=1)
    bm = tk.PhotoImage(file = 'null_data.png')
    bm1 = tk.PhotoImage(file = 'null_data.png')
    bm2 = tk.PhotoImage(file = 'null_data.png')
    bm3 = tk.PhotoImage(file = 'null_data.png')
    device1_name = tk.Label(window, text="感測器未連結", fg = "gray", font=('Microsoft JhengHei', 21), width=30, height=1,anchor = 'w')
    device1_name.grid(row=9,column=3,columnspan=2)
    device2_name = tk.Label(window, text="感測器未連結", fg = "gray", font=('Microsoft JhengHei', 21), width=30, height=1,anchor = 'w')
    device2_name.grid(row=9,column=5,columnspan=2)
    device1_Data = tk.Label(window,image = bm,width=475, height=165,relief="ridge")
    device1_Data.grid(row=10,column=3,columnspan=2,rowspan=4)
    device2_Data = tk.Label(window,image = bm1,width=475, height=165,relief="ridge")
    device2_Data.grid(row=10,column=5,columnspan=2,rowspan=4)
    device3_name = tk.Label(window, text="感測器未連結", fg = "gray", font=('Microsoft JhengHei', 21), width=30, height=1,anchor = 'w')
    device3_name.grid(row=14,column=3,columnspan=2)
    device4_name = tk.Label(window, text="感測器未連結", fg = "gray", font=('Microsoft JhengHei', 21), width=30, height=1,anchor = 'w')
    device4_name.grid(row=14,column=5,columnspan=2)
    device3_Data = tk.Label(window,image = bm2,width=475, height=165,relief="ridge")
    device3_Data.grid(row=15,column=3,columnspan=2,rowspan=3)
    device4_Data = tk.Label(window,image = bm3,width=475, height=165,relief="ridge")
    device4_Data.grid(row=15,column=5,columnspan=2,rowspan=3)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB',20), width=1, height=1).grid(row=1,column=7)
    control_label = tk.LabelFrame(window,width=50, height=10, text='控制面板', font=('Microsoft JhengHei', 21),padx=8)
    control_label.grid(row=1,column=8,rowspan=4,columnspan = 4)
    init_button = tk.Button(control_label, text='開啟雲端分析',font=('DFKai-SB',18),width=20, height=1,command=start_button)
    init_button.grid(row=0,column=0)
    init_button = tk.Button(control_label, text='關閉雲端分析',font=('DFKai-SB',18),width=20, height=1,command=end_button)
    init_button.grid(row=1,column=0)
    report_label = tk.LabelFrame(window,width=50, height=10, text='異常報告', font=('Microsoft JhengHei', 21),padx=8)
    report_label.grid(row=5,column=8,rowspan=13,columnspan = 4)
    tk.Label(report_label, text="異常區段：", fg = "gray", font=('Microsoft JhengHei', 16), width=20, height=1,anchor = 'w').grid(row=0,column=0)
    report_lab = tk.Label(report_label, text="     [無]", fg = "gray", font=('Microsoft JhengHei', 16), width=20, height=1,anchor = 'w')
    report_lab.grid(row=1,column=0)
    tk.Label(report_label, text="異常發生時間：", fg = "gray", font=('Microsoft JhengHei', 16), width=20, height=1,anchor = 'w').grid(row=2,column=0)
    report_lab1 = tk.Label(report_label, text="     [無]", fg = "gray", font=('Microsoft JhengHei', 16), width=20, height=1,anchor = 'w')
    report_lab1.grid(row=3,column=0)
    tk.Label(report_label, text="異常狀況：", fg = "gray", font=('Microsoft JhengHei', 16), width=20, height=1,anchor = 'w').grid(row=4,column=0)
    report_plot = tk.PhotoImage(file = 'abn_null.png')
    report_plot_zone = tk.Label(report_label,image = report_plot,relief="sunken",borderwidth=3,compound="right")
    report_plot_zone.grid(row=5,column=0)
    tk.Label(report_label, text="", fg = "gray", font=('Microsoft JhengHei', 8), width=20, height=1,anchor = 'w').grid(row=6,column=0)
    release_button = tk.Button(report_label, text='異常排除',font=('DFKai-SB',18),width=16, height=4,command=release)
    release_button.grid(row=7,column=0)
    tk.Label(report_label, text="", fg = "gray", font=('Microsoft JhengHei', 8), width=20, height=1,anchor = 'w').grid(row=8,column=0)
    GUIflag = True
    window.mainloop()


gui = threading.Thread(target = GUI)
gui.start()
while True:
    try:
        console_list.insert(0, "系統已啟動")
        break
    except:
        pass

global fig,data_lim,fig1,fig2,figa
data_lim=0
plt.style.use('bmh')
figa = plt.figure("fa")
figa.set_size_inches(2.52,2.4)
fig = plt.figure("f1")
fig.set_size_inches(6.4,2.2)
fig1 = plt.figure("f2",figsize=(3,3))
def on_connect(client, userdata, flags, rc):
    global connflag
    client.subscribe("EdgeComputingForAbnormalDetection/Publish/DeviceMessage", 1 )
    client.subscribe("EdgeComputingForAbnormalDetection/Publish/ComputingModel", 1 )
    client.subscribe("EdgeComputingForAbnormalDetection/Publish/DynamicReport", 1 )
    client.subscribe("EdgeComputingForAbnormalDetection/Publish/DataFlow", 1 )
    client.subscribe("EdgeComputingForAbnormalDetection/Publish/Command", 1 )
    console_list.insert(0, "等候連結檢測設備..")
    connflag = True
    
def on_message(client, userdata, msg):
    global model_plot,bm,device1_Data,fig,max_lim,report_plot,report_plot_zone,fig1,fig2,figa
    message = json.loads(msg.payload.decode('utf-8'))
    """
    try:
        mes = message["LSTM"]
        #print(mes)
    except:
        pass
    """
    try:
        i = message["x"]
        cycle_label["text"] = i
    except:
        pass
    try:
        i = message["y"]
        max_lim = float(i)
    except:
        pass
    try:
        datas = message["datas"]
        fig = plt.figure("f1")
        plt.clf()
        plt.style.use('dark_background')
        ax= fig.add_subplot(111)
        ax.set_ylim((0,1024))
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_xlim((0,max_lim*2))
        a,b,c,d=[],[],[],[]
        for i in datas:
            i = i.split(',')
            if len(i) == 4:
                a.append(float(i[0]))
                b.append(  (float(i[1])/4)*(36/1024)*10+400  )
                c.append(float(i[2])*5)
                d.append(( float(i[3])**0.8) + 100 )
        ax.plot(range(len(a)),a,color ="red",linewidth=1)
        ax.plot(range(len(b)),b,color = "blue",linewidth=1)
        ax.plot(range(len(c)),c,color = "green",linewidth=1)
        ax.plot(range(len(d)),d,color = "yellow",linewidth=1)
        fig.savefig("PLOR.png",pad_inches = 0,bbox_inches="tight")
        bm = tk.PhotoImage(file = "PLOR.png")
        device1_Data["image"] = bm
        print("plot")
    except:
        pass
    try:
        mes = message["Uconsole"]
        mes = mes.split(':')[1]
        data_line = datetime.datetime.utcfromtimestamp(int(mes))
        data_line = data_line.strftime("%M:%S")
        console_list1.insert(0,"發送數據("+str(data_line)+")")
    except:
        pass
    try:
        mes = message["Dconsole"]
        lambda_table.insert('',"0",text='',values=(str(int(mes["timestamp"])),"927",str(int(time.time()-float(mes["timestamp"])))))
        if mes["abnormal_section"] == [[],[]]:
            data_line = datetime.datetime.utcfromtimestamp(int(float(mes["timestamp"])))
            data_line = data_line.strftime("%M:%S")
            console_list2.insert(0,'(數據 '+str(data_line)+")分析結果：正常")
        else:
            upd = False
            fig1 = plt.figure("f2",figsize=(2,2))
            plt.style.use('classic')
            plt.clf()
            ax1 = fig1.add_subplot(111)
            for i in message['abnormal_list']:
                x,y,z,n=[],[],[],[]
                if len(i) >= 40 and len(i) <= 150:
                    for j in i:
                        j = j.split(',')
                        x.append(float(j[0]))
                        y.append((float(j[1])/4)*(36/1024)*10+400)
                        z.append(float(j[2])*5)
                        n.append((float(j[3])**0.8) + 100)
                    plt.cla()
                    ax1.plot(range(len(x)),x,color ="red",linewidth=1)
                    ax1.plot(range(len(y)),y,color ="blue",linewidth=1)
                    ax1.plot(range(len(z)),z,color ="green",linewidth=1)
                    ax1.plot(range(len(n)),n,color ="yellow",linewidth=1)
                    ax1.plot([len(i),len(i)],[1024,1024],color ="white",linewidth=3)
                    upd = True
            ax1.set_ylim((0,1024))
            ax1.set_yticks([])
            ax1.set_xticks([])
            fig1.savefig("abn_plt.png",pad_inches = 0,bbox_inches="tight")
            report_plot = tk.PhotoImage(file = "abn_plt.png")
            report_plot_zone["image"] = report_plot
            
            if upd == True:
                report_lab["text"] = "     "+str(mes["abnormal_section"])
                data_line = datetime.datetime.utcfromtimestamp(int( float(mes["timestamp"]) + float(int(mes["abnormal_section"][0][0])/36.0)   ))
                data_line = data_line.strftime("%M:%S")
                report_lab1["text"] = "     "+str(data_line)
                data_line = datetime.datetime.utcfromtimestamp(int(float(mes["timestamp"])))
                data_line = data_line.strftime("%M:%S")
                console_list2.insert(0,'(數據 '+str(data_line)+")分析結果：異常  請檢查異常報告")
            else:
                data_line = datetime.datetime.utcfromtimestamp(int(float(mes["timestamp"])))
                data_line = data_line.strftime("%M:%S")
                console_list2.insert(0,'(數據 '+str(data_line)+")分析結果：警示")
                TOPIC_Value = json.dumps({"startflag":"c"})
                mqttc.publish("EdgeComputingForAbnormalDetection/Subscribe",TOPIC_Value, qos=1)
                
    except:
        pass
    
    try:
        me = str(float(message["memory"]))
        memory_label["text"] = me+" %"
        hz = str(int(float(message["hz"])))
        peremeter_label["text"] = hz+" Hz"
    except:
        pass
    try:
        v = message["vendor"]
        d = message["device"]
        c = message["cert"]
        vendor_label["text"] = v
        device_label["text"] = d
        cert_label["text"] = c
        console_list.insert(0, "設備已連結,正在進行設定")
    except:
        pass
    try:
        n = message['devices']
        device1_name["text"] = message['devices'][0]
        device1_name["fg"] = "black"
        device2_name["text"] = message['devices'][1]
        device2_name["fg"] = "black"
        device3_name["text"] = message['devices'][2]
        device3_name["fg"] = "black"
        device4_name["text"] = message['devices'][3]
        device4_name["fg"] = "black"
    except:
        pass
    try:
        vx = message["x"]
        model_plot.setdefault("x",message["x"])
    except:
        pass
    try:
        vy = message["y"]
        model_plot.setdefault("y",message["y"])
    except:
        pass
    try:
        mx = message["Model_x"]
        model_plot.setdefault("mx",message["Model_x"])
    except:
        pass
    try:
        my = message["Model_y"]
        model_plot.setdefault("my",message["Model_y"])
        with open("lambda_plot4.json",'r') as f:
            ld = json.load(f)
        while True:
            global lambda_runtime,lambda_runtime_plot
            if len(model_plot) == 4:
                figa = plt.figure("fa")
                plt.style.use('bmh')
                Model_x,Model_y = [],[]
                for i in ld:
                    Model_x.append(float(i[1]))
                    Model_y.append(float(i[2]))
                plt.plot(Model_y,Model_x,color="darkblue")
                plt.plot([0,30],[927,927],color="red",linestyle="--",linewidth=1)
                plt.plot([30,30],[0,927],color="dimgray",linestyle="--",linewidth=1)
                plt.xticks(fontsize=7)
                plt.yticks(fontsize=7)
                plt.xlim([0,60])
                plt.ylim([0,2000])
                figa.savefig("lambda_runtime_plot.png",dpi=100)
                time.sleep(1)
                lambda_runtime = tk.PhotoImage(file = 'lambda_runtime_plot.png')
                lambda_runtime_plot["image"] = lambda_runtime
                console_list.insert(0, "初始化完成")
                console_list.insert(0, "開始採集數據...")
                max_m = int(float(model_plot["y"])/float(model_plot["x"]))
                peremeter_label["text"] = str(max_m)+" Hz."
                break
            else:
                pass
    except:
        pass

vendor = "SiMSlab"
device = "Laptop"
cert = "1b598504c9"
sys = {"vendor":vendor,"device":device,"cert":cert}
mqttc = paho.Client()                      
mqttc.on_connect = on_connect
mqttc.on_message = on_message
awshost = "azzt8jgouxwto-ats.iot.us-east-2.amazonaws.com"
awsport = 8883                                             
clientId = sys["vendor"]                                   
thingName = sys["vendor"]+"_"+sys["device"]
caPath = "C:/Users/b1040/Desktop/Edge_Computing_For_Abnormal_Detection/certs/AmazonRootCA1.pem"                           
certPath = "C:/Users/b1040/Desktop/Edge_Computing_For_Abnormal_Detection/certs/"+sys["cert"]+"-certificate.pem.crt"                           
keyPath = "C:/Users/b1040/Desktop/Edge_Computing_For_Abnormal_Detection/certs/"+sys["cert"]+"-private.pem.key" 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_start()

while True:
    if connflag == True:
        pass
        break
