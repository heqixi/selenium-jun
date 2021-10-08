# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 12:52:58 2021

@author: Raytine
"""
# -*-coding:utf-8-*-
import time, datetime
import threading
from tkinter import *
from tkinter import ttk
from Application import Application as Task
import pandas as pd


class A:
    def __init__(self, master=None):
        self.root = master
        self.root.geometry('1000x800+200+200')
        self.root.title('测试')
        self.log_meassge=[[],[],[]]
        # self.root.bind("<Motion>", self.call_back)
        self.frm1 = Frame(self.root)
        self.frm2 = Frame(self.root)
        self.frm3 = Frame(self.root)
        self.create_page_main()
        self.create_page_left_sider()
        self.create_page_top()
        self.create_menu()

    def call_back(self, event):
        print('现在的位置是：', event.x_root, event.y_root)
    
    def log(self, level, message):
        if level == 'i':
            self.log_meassge[0].append(message)
            Label(self.frm1, text="\n".join(self.log_meassge[0])).place(x=0, y=500, width=800)
        elif level == 'w':
            self.log_meassge[1].append(message)
            Label(self.frm1, text="\n".join(self.log_meassge[1])).place(x=0, y=600, width=800)
        else:
            self.log_message[2].append(message)
            Label(self.frm1, text="\n".join(self.log_meassge[2])).place(x=0, y=700, width=800)

    def create_page_main(self):
        self.frm1.config(bg='white', height=800, width=800)
        Label(self.frm1, text='创建任务').place(in_=self.frm1, anchor=NW)
        self.frm1.place(x=180, y=50)
                # frm1下的控件
        #Label(self.frm1, text='项目资源管理平台',
        #      fg='red', font='Verdana 10 bold').place(x=100, y=50, height=80, width=400)
        combobox = ttk.Combobox(self.frm1, height=30, width=20, state='readonly', values=['随机用户','heqixi', 'heqigang'])
        combobox.current(0)
        combobox.place(x=10, y=20)
        
        #选择开始和结束
        params={"user_name":"HUA", "password":"asdf?135","start_port_search_key":"上海",
                "start_port_match_key":"上海-Shanghai","dest_port_search_key":"汉堡",
                "dest_port_match_key":"汉堡-Hamburg","box_style":"40HQ",
                "task_start_time": datetime.datetime.now() + datetime.timedelta(minutes=1)}
        tasks = []
        def generate_task():
            task = Task(params, self)
            try:
                taskThread = threading.Thread(target=task.start)
                taskThread.start()
            except Exception as e:
                messagebox.askretrycancel(title="出错了", message=e)
            else:
                tasks.append(task)
        Button(self.frm1, text='生成任务', height=2, width=8, command=generate_task).place(x=200, y=200)
        
    def create_page_left_sider(self):
        self.frm2.config(bg='gray', height=800, width=150)
        self.frm2.place(x=20, y=50)
        
        def validate_user_name():
            if len(user_name_input.get().strip()) <= 0:
                return False
            else:
                return True
        Label(self.frm2, text='用户名').place(x=0,y=0, height=20, width=50)
        user_name_input=Entry(self.frm2, validatecommand=validate_user_name)
        user_name_input.place(x=0, y=20, height=30, width=130)
        Label(self.frm2, text='密码').place(x=0,y=60, height=15, width=50)
        password_input=Entry(self.frm2)
        password_input.place(x=0, y=75,height=30, width=130)
        checkout_out_pw_input=Entry(self.frm2)
        Label(self.frm2, text='支付密码').place(x=0,y=115, height=15, width=50)
        checkout_out_pw_input.place(x=0, y=130, height=30,width=130)
        userName="fa"
        password="ad"
        checkoutPassword="da"
        #userFile = open("./users.text", 'w')
        users = []
        users_file_handlers = open("./users.text", 'r')
        for line in users_file_handlers.readlines():
            print(line)
            user = line.strip('\n').split(',')
            if len(user) < 3 or len(user[0]) <=0 or len(user[1])<=0 or len(user[2]) <=0:
                print("invalid user")
                continue
            users.append(user)
        def isUserExist(user_name):
            if len(user_name) <=0:
                return False
            for user in users:
                print(user[0])
                if (user_name == user[0]):
                    return True
            return False
        def writeUser(users):
            if len(users) <= 0:
                return
            users_file_write_handlers = open("./users.text", 'w')
            for user in users:
                users_file_write_handlers.writelines(",".join(user) + "\n")
        def saveCommand():
            userName=user_name_input.get()
            password=password_input.get()
            checkoutPassword=checkout_out_pw_input.get()
            if len(userName.strip()) <= 0:
                print("user name is invalid")
                messagebox.askretrycancel(title="无效用户", message="无效用户名")
            elif len(password.strip()) <= 0:
                print("password is invalid")
                messagebox.askretrycancel(title="无效用户", message="无效登录密码")
                return
            elif len(checkoutPassword.strip()) <= 0:
                print("checkout password is invalid")
                messagebox.askretrycancel(title="无效用户", message="无效支付密码")
                return
            elif isUserExist(userName):
                print("user exist, modif")
                result=messagebox.askokcancel(title="用户已存在", message="覆盖原有用户？")
                if not result:
                    return
                for i in range(len(users)):
                    if (userName == users[i][0]):
                        users[i] = [userName, password, checkoutPassword]
                        break
                writeUser(users)
            else:
                print("valid parameters")
                print(userName + password + checkoutPassword)
                users.append([userName, password, checkoutPassword])
                writeUser(users)
        Button(self.frm2, text='保存新用户', command=saveCommand).place(x=20, y=170, width=80)
    
        

        
    def create_page_top(self):
        self.frm3.config(bg='yellow', height=40, width=1000)
        Label(self.frm3, text='frm3').place(in_=self.frm3, anchor=NW)
        self.frm3.place(x=20, y=5)
        # frm3下的Label
        Label(self.frm3, text='Label Test Test',
              fg='red', font='Verdana 10 bold').place(x=300, y=10)

    def create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label='测试1', menu=filemenu)
        filemenu.add_command(label='1')
        filemenu.add_command(label='2')
        filemenu.add_command(label='3')

        onemenu = Menu(menu)
        menu.add_cascade(label='测试2', menu=onemenu)
        onemenu.add_command(label='1')
        onemenu.add_command(label='2')
        onemenu.add_command(label='3')


if __name__ == '__main__':
    root = Tk()
    A(root)
    mainloop()