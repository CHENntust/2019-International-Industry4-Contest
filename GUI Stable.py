import os
import time
import threading
from threading import Thread
import tkinter as tk
from tkinter import ttk
import psutil
import pickle
import paho.mqtt.client as paho
import ssl
import socket
import serial
import numpy as np
import boto3
import json
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

GUIflag = False
start_f = False
startflag = False
sgflag = False
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom=geom

first_initial = False
def start():
    global startflag,start_f
    if start_f == False:
        start_f = True
    else:
        startflag = True
        
def get_entry():
    global int_input
    var = e.get()
    root.destroy()
    int_input = int(var)
    return var

def initial():
    global Model,Model_y,Model_x,first_initial,lambda_img
    console_list.insert(0, "獲取系統平衡擷取參數")
    sub_GUI()
    console_list.insert(0, "建立效能分析模型")
    with open('models/knn.pickle', 'rb') as f:
        Model = pickle.load(f)  
    plt.style.use('bmh')
    if first_initial == False:
        first_initial = True
        fig = plt.figure()
        fig.set_size_inches(2.52,2.4)
        Model_x,Model_y=[],[]
        for j in range(50):
            Model_y.append(j*4)
            Model_x.append(Model.predict(np.array([[8,j*4]]))[0])
        plt.plot(Model_y,Model_x,color="darkblue")
        ver_x,ver_y,horiz_x,horiz_y=[],[],[],[]
        for i in range(int(Model.predict(np.array([[8,int_input*5]]))[0])):
            ver_x.append(i)
            ver_y.append(int_input*5)
        plt.plot(ver_y,ver_x,color="dimgray",linestyle="--",linewidth=1)
        for i in range((int_input*5)):
            horiz_x.append(Model.predict(np.array([[8,int_input*5]]))[0])
            horiz_y.append(i)
        plt.plot(horiz_y,horiz_x,color="red",linestyle="--",linewidth=1) 
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
        fig.savefig("lambda_runtime_plot.png",dpi=100)
        time.sleep(1)
        lambda_img = tk.PhotoImage(file = 'lambda_runtime_plot.png')
        lambda_runtime_plot["image"] = lambda_img
    console_list.insert(0, "初始化完成 [點即啟動]")
    return int_input

    
def sub_GUI():
    global e,root
    root = tk.Tk()
    root.title('設置參數')
    #root.geometry("240x90")
    def center_window(w, h):
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    center_window(240, 90)

    la = tk.Label(root,text=" ",font=('DFKai-SB', 8),width=5)
    la.grid(row=0,column=0)
    la = tk.Label(root,text=" ",font=('DFKai-SB', 8),width=5)
    la.grid(row=0,column=1)
    la = tk.Label(root,text=" ",font=('DFKai-SB', 8),width=5)
    la.grid(row=0,column=2)
    e = tk.Entry(root,width=18)
    e.grid(row=1,column=1)
    but = tk.Button(root,width=12,text="輸入",font=('DFKai-SB', 12),command=get_entry)
    but.grid(row=2,column=1)
    root.mainloop()
    

def GUI():
    global GUIflag,console_list,console_list1,console_list2,vendor_label,device_label,cert_label,cycle_label,peremeter_label
    global lambda_runtime_plot,device1_Data,memory_label,lambda_table,device1_name,device2_name,device3_name,device4_name
    window = tk.Tk()
    window.title('異質檢測之邊緣運算解決方案')
    app=FullScreenApp(window)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 1), width=15, height=1).grid(row=0,column=0)
    tk.Label(window, text="廠商代號：", fg = "black", font=('DFKai-SB', 21), width=11, height=1,anchor = 'e').grid(row=1,column=0)
    vendor_label = tk.Label(window, text="", fg = "dimgray", font=('Arial', 18), width=15, height=1,relief="groove",borderwidth=3,anchor = 'w')
    vendor_label.grid(row=1,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 1), width=17, height=1).grid(row=2,column=0)
    tk.Label(window, text="設備名稱：", fg = "black", font=('DFKai-SB', 21), width=11, height=1,anchor = 'e').grid(row=3,column=0)
    device_label = tk.Label(window, text="", fg = "dimgray", font=('Arial', 18), width=15, height=1,relief="groove",borderwidth=3,anchor = 'w')
    device_label.grid(row=3,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 1), width=17, height=1).grid(row=4,column=1)
    tk.Label(window, text="憑證編號：", fg = "black", font=('DFKai-SB', 21), width=11, height=1,anchor = 'e').grid(row=5,column=0)
    cert_label = tk.Label(window, text="", fg = "dimgray", font=('Arial', 18), width=15, height=1,relief="groove",borderwidth=3,anchor = 'w')
    cert_label.grid(row=5,column=1)
    tk.Label(window, text="", fg = "black", font=('Microsoft JhengHei', 1), width=15, height=1).grid(row=6,column=0)
    tk.Label(window, text="記憶體使用量：", fg = "black", font=('DFKai-SB', 21), width=11, height=1,anchor = 'e').grid(row=7,column=0)
    memory_label = tk.Label(window, text="", fg = "black", font=('Arial', 18), width=15, height=1,relief="groove",borderwidth=3,anchor = 'w')
    memory_label.grid(row=7,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 1), width=15, height=1).grid(row=8,column=0)
    tk.Label(window, text="系統週期：", fg = "black", font=('DFKai-SB', 21), width=11, height=1,anchor = 'e').grid(row=9,column=0)
    cycle_label = tk.Label(window, text="", fg = "black", font=('Arial', 18), width=15, height=1,relief="groove",borderwidth=3,anchor = 'w')
    cycle_label.grid(row=9,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB', 1), width=15, height=1).grid(row=10,column=0)
    tk.Label(window, text="採集頻率：", fg = "black", font=('DFKai-SB', 21), width=11, height=1,anchor = 'e').grid(row=11,column=0)
    peremeter_label = tk.Label(window, text="", fg = "black", font=('Arial', 18), width=15, height=1,relief="groove",borderwidth=3,anchor = 'w')
    peremeter_label.grid(row=11,column=1)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB',12), width=15, height=1).grid(row=12,column=0)
    lambda_img = tk.PhotoImage(file = "lambda_runtime_plot.png")
    lambda_label = tk.LabelFrame(window,width=50, height=10, text='雲端運算效能模型', font=('Microsoft JhengHei', 14),padx=8)
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
    tk.Label(window, text="", fg = "black", font=('Arial', 18), width=3, height=1).grid(row=1,column=2)
    console_label = tk.LabelFrame(window,width=50, height=10, text='動態分析報告', font=('Microsoft JhengHei', 14),padx=8)
    console_label.grid(row=1,column=3,rowspan=7,columnspan = 4)
    console_list = tk.Listbox(console_label,width=17, height=8, font=('Microsoft JhengHei', 12), fg = "blue")
    console_list.grid(row=0,column=2)
    console_list1 = tk.Listbox(console_label,width=26, height=8, font=('Microsoft JhengHei', 12), fg = "blue")
    console_list1.grid(row=0,column=0)
    console_list2 = tk.Listbox(console_label,width=42, height=8, font=('Microsoft JhengHei', 12), fg = "blue")
    console_list2.grid(row=0,column=1)
    bm = tk.PhotoImage(file = 'null_data.png')
    bm1 = tk.PhotoImage(file = 'null_data.png')
    bm2 = tk.PhotoImage(file = 'null_data.png')
    bm3 = tk.PhotoImage(file = 'null_data.png')
    device1_name = tk.Label(window, text="感測器未連結", fg = "gray", font=('Microsoft JhengHei', 18), width=28, height=1,anchor = 'w')
    device1_name.grid(row=9,column=3,columnspan=2)
    device2_name = tk.Label(window, text="感測器未連結", fg = "gray", font=('Microsoft JhengHei', 18), width=28, height=1,anchor = 'w')
    device2_name.grid(row=9,column=5,columnspan=2)
    device1_Data = tk.Label(window,image = bm,width=400, height=135,relief="ridge")
    device1_Data.grid(row=10,column=3,columnspan=2,rowspan=4)
    device2_Data = tk.Label(window,image = bm1,width=400, height=135,relief="ridge")
    device2_Data.grid(row=10,column=5,columnspan=2,rowspan=4)
    device3_name = tk.Label(window, text="感測器未連結", fg = "gray", font=('Microsoft JhengHei', 18), width=28, height=1,anchor = 'w')
    device3_name.grid(row=14,column=3,columnspan=2)
    device4_name = tk.Label(window, text="感測器未連結", fg = "gray", font=('Microsoft JhengHei', 18), width=28, height=1,anchor = 'w')
    device4_name.grid(row=14,column=5,columnspan=2)
    device3_Data = tk.Label(window,image = bm2,width=400, height=135,relief="ridge")
    device3_Data.grid(row=15,column=3,columnspan=2,rowspan=3)
    device4_Data = tk.Label(window,image = bm3,width=400, height=135,relief="ridge")
    device4_Data.grid(row=15,column=5,columnspan=2,rowspan=3)
    tk.Label(window, text="", fg = "black", font=('DFKai-SB',20), width=2, height=1).grid(row=1,column=7)
    control_label = tk.LabelFrame(window,width=50, height=10, text='控制面板', font=('Microsoft JhengHei', 14),padx=8)
    control_label.grid(row=1,column=8,rowspan=10,columnspan = 4)
    init_button = tk.Button(control_label, text='啟動',font=('DFKai-SB',15),width=20, height=1,command=start)
    init_button.grid(row=0,column=0)
    init_button = tk.Button(control_label, text='系統重置',font=('DFKai-SB',15),width=20, height=1,command=sub_GUI)
    init_button.grid(row=1,column=0)
    init_button = tk.Button(control_label, text='關閉程式',font=('DFKai-SB',15),width=20, height=1,command=initial)
    init_button.grid(row=2,column=0)
    init_button = tk.Button(control_label, text='系統重置',font=('DFKai-SB',15),width=20, height=1,command=initial)
    init_button.grid(row=3,column=0)
    init_button = tk.Button(control_label, text='系統重置',font=('DFKai-SB',15),width=20, height=1,command=initial)
    init_button.grid(row=4,column=0)
    init_button = tk.Button(control_label, text='系統重置',font=('DFKai-SB',15),width=20, height=1,command=initial)
    init_button.grid(row=5,column=0)
    GUIflag = True
    window.mainloop()

gui = threading.Thread(target = GUI)
gui.start()

global total_data_dict
connflag = False
total_data_dict = {}
def GPIO_control(status):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(3,GPIO.OUT)
    GPIO.setup(5,GPIO.OUT)
    GPIO.setup(7,GPIO.OUT)
    if status[0] == "Green":
        l = [5,3,7]
    elif status[0] == "Blue":
        l = [7,3,5]
    else:
        l = [3,5,7]
    if status[1] =="close":
        GPIO.output(l[0], GPIO.LOW)
        GPIO.output(l[1], GPIO.LOW)
        GPIO.output(l[2], GPIO.LOW)
    else:
        GPIO.output(l[0], GPIO.HIGH)
        GPIO.output(l[1], GPIO.LOW)
        GPIO.output(l[2], GPIO.LOW)
        
def get_init_data():
    with open("sys.json","r") as f:
        sys = json.load(f)
    if sys["cert"] != "":
        pass
    else:
        while True:
            #vendor = input("輸入廠商名稱")
            #device = input("輸入設備名稱 ")
            #cert = input("輸入憑證編號")
            vendor = "SiMSlab"
            device = "RaspberryPi_32G"
            cert = "b9c38f898c"
            s3 = boto3.resource('s3')
            try:
                s3.meta.client.download_file("edge-computing-for-abnormal-detection",vendor+"/"+device+"_certs/AmazonRootCA1.pem", "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/AmazonRootCA1.pem")
                s3.meta.client.download_file("edge-computing-for-abnormal-detection",vendor+"/"+device+"_certs/"+cert+"-certificate.pem.crt", "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/"+cert+"-certificate.pem.crt")
                s3.meta.client.download_file("edge-computing-for-abnormal-detection",vendor+"/"+device+"_certs/"+cert+"-private.pem.key", "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/"+cert+"-private.pem.key")
                s3.meta.client.download_file("edge-computing-for-abnormal-detection",vendor+"/"+device+"_certs/"+cert+"-public.pem.key", "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/"+cert+"-public.pem.key")
                del s3
                with open("sys.json","w") as f:
                    sys = {"vendor":vendor,"device":device,"cert":cert}
                    json.dump(sys, f)
                break
            except:
                pass
    return sys

def get_devices():
    console_list.insert(0, "感測器環境設定")
    devices = {}
    try:
        Arduino0 = serial.Serial('/dev/ttyACM0', 9600)
        devices.setdefault("ttyACM0",Arduino0)
        device1_name["text"]="ttyACM0"
        device1_name["fg"]="black"
    except:
        pass
    try:
        Arduino1 = serial.Serial('/dev/ttyACM1', 9600)
        devices.setdefault("ttyACM1",Arduino1)
        device2_name["text"]="ttyACM1"
        device2_name["fg"]="black"
    except:
        pass
    try:
        Arduino2 = serial.Serial('/dev/ttyACM2', 9600)
        devices.setdefault("ttyACM2",Arduino2)
        device3_name["text"]="ttyACM2"
        device3_name["fg"]="black"
    except:
        pass
    try:
        Arduino3 = serial.Serial('/dev/ttyACM3', 9600)
        devices.setdefault("ttyACM3",Arduino3)
        device4_name["text"]="ttyACM3"
        device4_name["fg"]="black"
    except:
        pass
    return devices

def save_plot(ax,datas):
    d1,d2,d3,d4=[],[],[],[]
    for j in datas:
        j = j.split(',')
        if len(j) >= 4:
            try:
                d1.append(int(j[0]))
                d2.append(int(j[1]))
                d3.append(int(j[2]))
                d4.append(int(j[3]))
            except:
                pass
    ax.plot(range(len(d1)),d1,color="yellow",linewidth=1)
    ax.plot(range(len(d2)),d2,color="green",linewidth=1)
    ax.plot(range(len(d3)),d3,color="red",linewidth=1)
    ax.plot(range(len(d4)),d4,color="blue",linewidth=1)
    fig1.savefig("PLOR.png",pad_inches = 0,bbox_inches="tight")

def create_batch(devices,batch,batch_time,lim):
    import time
    count = 0
    ax= plt.subplot(111)
    ax.set_ylim((0,1024))
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlim((0,lim))
    datas = {}
    dimension = len(devices)
    for i in devices:
        datas.setdefault(i,list())
    timestamp = time.time()
    #last = timestamp
    end_stamp = timestamp + batch_time
    div = 10
    while time.time() <= end_stamp:
        if int(time.time())%2 ==1:
            GPIO_control(status =["Green","open"])
        else:
            GPIO_control(status =["Green","close"])
        for i in devices:
            try:
                if str(devices[i].readline().decode('utf-8').strip('\r\n')) != "":
                    datas[i].append(str(devices[i].readline().decode('utf-8').strip('\r\n')))
            except:
                pass
        
        for i in datas:
            if len(datas[i])%50 ==0:
                div = div*1.1
                #print(time.time()-last)
                #last = time.time()
            if int(len(datas[i])%div) == 1:
                sp = threading.Thread(target = save_plot(ax,datas[i]))
                sp.start()
                bm = tk.PhotoImage(file = "PLOR.png")
                device1_Data["image"] = bm
    plt.clf()
    return timestamp,dimension,datas

def on_connect(client, userdata, flags, rc):
    global connflag
    client.subscribe("EdgeComputingForAbnormalDetection/Subscribe/"+sys["cert"], 1 )
    console_list.insert(0, "AWS IoT連線完成")
    connflag = True
    
def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    time_delay = int(time.time() - float(message["timestamp"])-batch_time)
    status="Normal"
    console_list2.insert(0, "Stamp:"+str(int(message["timestamp"]))+"("+status+")")
    lambda_table.insert('',"0",text='',values=(str(int(message["timestamp"])),str(len(total_data_dict[str(message["timestamp"])][message["sensor"]])),str(time_delay)))
    print(message)
    #print(total_data_dict[str(message["timestamp"])])
    print("--------------------")
while True:
    if GUIflag == True:
        GPIO_control(status = ["Blue","open"])
        sys = get_init_data()
        console_list.insert(0, "獲取系統啟動資訊")
        vendor_label["text"] = sys["vendor"]
        device_label["text"] = sys["device"]
        cert_label["text"] = sys["cert"]
        mqttc = paho.Client()                      
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        awshost = "azzt8jgouxwto-ats.iot.us-east-2.amazonaws.com"
        awsport = 8883                                             
        clientId = sys["vendor"]                                   
        thingName = sys["vendor"]+"_"+sys["device"]
        caPath = "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/AmazonRootCA1.pem"                           
        certPath = "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/"+sys["cert"]+"-certificate.pem.crt"                           
        keyPath = "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/"+sys["cert"]+"-private.pem.key" 
        mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
        mqttc.connect(awshost, awsport, keepalive=60)
        mqttc.loop_start()
        while True:
            if connflag == True:
                GPIO_control(status = ["Green","open"])
                devices = get_devices()
                period = initial()
                while True:
                    if startflag == True:
                        batch_time = period * 5
                        info = psutil.virtual_memory()
                        memory_label["text"] = str(round(info.percent,2))+" %"
                        with open('models/knn.pickle', 'rb') as f:
                            Model = pickle.load(f)
                        batch = Model.predict(np.array([[4,batch_time]]))[0]
                        lim = batch
                        cycle_label["text"] = str(batch_time)
                        peremeter_label["text"] = str(int(batch/batch_time))+" Hz."
                        console_list.insert(0, "開始採集數據")
                        global fig1
                        plt.style.use('dark_background')
                        fig1 = plt.figure()
                        fig1.set_size_inches(5.2,1.8)
                        while True:
                            timestamp,dimension,datas =  create_batch(devices,batch,batch_time,lim)
                            for i in datas:
                                data_len = len(datas[i])
                                lim = data_len
                                peremeter_label["text"] = str(int(data_len/batch_time))+" Hz / (Max:"+str(int(batch/batch_time))+")"
                                for i in datas:
                                    data = datas[i]
                                    TOPIC_Value = json.dumps({"timestamp":timestamp,"cert":sys["cert"],"sensor":i,"data":data})
                                    total_data_dict.setdefault(str(timestamp),{i:data})
                                    console_list1.insert(0,"["+str(i)+"] Stamp:"+str(int(timestamp)))
                                    mqttc.publish("EdgeComputingForAbnormalDetection/Publish",TOPIC_Value, qos=1)
                                    info = psutil.virtual_memory()
                                    memory_label["text"] = str(round(info.percent,2))+" %"
                    else:
                        pass
            else:
                pass
    else:
        pass
