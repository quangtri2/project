import tkinter as tk
from PIL import Image, ImageTk,ImageFilter
import cv2
from tkinter import ttk
import datetime
import numpy as np
from pyzbar.pyzbar import decode
from tkinter import messagebox
import cv2 as cv
import sys
import pyodbc as odbc
import traceback
import pandas as pd
import sys
import threading
from tkinter import filedialog
import serial


# Arduino_Serial = serial.Serial("COM6",9600)
# s = Arduino_Serial.readline()
  

data = 'xx'
data1=''
last_data = ''
conn = ""
ktraArd = 0
ktra = 0
ktratable = ''
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-9Q5LPOB\SQLEXPRESS'
DATABASE_NAME = 'KEP_Sv_DT'
directionOfQrCode = ''
connection_string = f"""
    DRIVER={DRIVER_NAME};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes
"""   

try:
    print("Đang kết nối với server ....")
    conn = odbc.connect(connection_string)
except:
    print("Kiểm tra lại cách kết nối nhaa")
    exit() #Thoát khỏi chương trình
else:
    print("Kết nối thành công!")

root = tk.Tk()
root.title("Nghiên cứu khoa học")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# Tính toán kích thước của cửa sổ
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

frame_width = window_width // 3  # Kích thước mỗi frame
frame_height = window_height

# Tạo 3 frame conn
frame1 = tk.Frame(root, width=frame_width, height=frame_height, bg="black")
frame1.pack_propagate(False)
frame1.grid(row=0, column=0)

frame2 = tk.Frame(root, width=frame_width*2, height=frame_height, bg="pink")
frame2.pack_propagate(False)
frame2.grid(row=0, column=1)

image_logo = Image.open("images.png")
image_logo = image_logo.resize(((frame_width), int(frame_height/2)))
# Chuyển đổi ảnh thành định dạng hợp lệ cho Tkinter
photo_logo = ImageTk.PhotoImage(image_logo)

# Tạo widget Label để hiển thị ảnh
label_logo = tk.Label(frame1, image=photo_logo)
label_logo.pack()

handle_frame_img = tk.Label(frame1,image='',width=frame_width,height=400)
handle_frame_img.place(x=0,y=400)
camera = cv2.VideoCapture(0)

counter = 1
# def add_data():
# # Lấy ngày/giờ hiện tại
#     global counter
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     # Thêm dữ liệu mới vào bảng
#     table.insert("", "end", text=str(counter), values=(f"Mã hàng {data[1]}","Nội dung {data[0]}","Ngày/Giờ{current_time}"))
#     counter += 1
  

#Hàm lấy dữ liệu từ database
# data_select = []
def selectData_dataBase(data):
    # global data_select
    sql_query = f"SELECT * FROM Bang_Tong_Kho Where MaHang = {data}"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        #Lấy dữ liệu từ database
        row = cursor.fetchone()
    except Exception as e:
        print(f"Lỗi lấy dữ liệu: {e}")
        traceback.print_exc()
    else:
        # Kiểm tra xem có dữ liệu được trả về không
        if row is not None:
        # Chuyển đổi dữ liệu thành list và gán vào biến
            data_select = [element for element in row]
            # print('Truy vấn dữ liệu thành công')
    return tuple(data_select)



##################################TrangTri############################################################################################
nameTT = ttk.Label(frame2,text="Nghiên cứu khoa học năm 2023 - 2024", font=("Arial", 30))
nameTT.place(x=200,y=15)

nameDeTai = ttk.Label(frame2,text="Đề tài", font=("Arial", 20))
nameDeTai.place(x=450,y=70)

nameDeTai = ttk.Label(frame2,text="Nghiên cứu xây dựng hệ Smart Factory cho cụm nhận dạng phân loại sản phẩm và lưu kho của nhà máy cơ khí", font=("Arial", 15))
nameDeTai.place(x=20,y=120)

nameNHD = ttk.Label(frame2,text="Người hướng dẫn: T.S PHẠM THỊ LÝ", font=("Arial", 15))
nameNHD.place(x=20,y=190)

nameLop = ttk.Label(frame2,text="Lớp: TĐH1 - K61", font=("Arial", 15))
nameLop.place(x=20,y=260)

##################################TrangTri############################################################################################



##################################ComboBox############################################################################################

colum_TongKho = ("0","1", "2","3","4","5","6")
colum_XuatKho = ("0","1", "2","3","4","5","6","7")
colum_NhapKho = ("0","1", "2","3","4","5","6","7")



nameTable = ttk.Label(frame2,text="Hãy chọn bảng",width=12, font=("Arial", 12))
nameTable.place(x=0,y=330)

table = ttk.Treeview(frame2, columns=colum_TongKho)
# table.heading("#0", text="STT")
# table.heading("0", text="Mã hàng")
# table.heading("1", text="Tên hàng")
# table.heading("2", text="Xuất xứ")
# table.heading("3", text="Giá nhập")
# table.heading("4", text="Giá xuất")
# table.heading("5", text="Số lượng")
# table.heading("6", text="Khu Vực")

# table.column("#0", width=150)
# table.column("6",widt=150)

# table.pack(fill="both",padx=0,pady=350)

nameTableData = tk.StringVar()
# nameTableData.set("Tong")


def setup_table(name, time_label = None):
    table.delete(*table.get_children())
    nameTable.config(text=name)
    table.config(columns=colum_NhapKho)
    table.heading("#0", text="STT")
    table.heading("0", text="Mã hàng")
    table.heading("1", text="Tên hàng")
    table.heading("2", text="Xuất xứ")
    table.heading("3", text="Giá nhập")
    table.heading("4", text="Giá xuất")
    table.heading("5", text="Số lượng")
    table.heading("6", text="Khu Vực")
    table.heading("7", text=time_label)
    table.column("#0", width=150)
    table.column("6", width=150)
    table.pack(fill="both", padx=0, pady=350)


def insertData(data,table):
    global conn
    global counter
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_query = ""
    time = str(current_time)
    data=tuple(data)
    data = data + (time,)
    # data.append(time)
    sql_query = f"INSERT INTO Bang_{table}_Kho (MaHang,TenHang,XuatXu,GiaNhap,GiaBan,SoLuong{table},KhuVuc,ThoiGian{table}) VALUES (?,?,?,?,?,?,?,?)"      
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query,data)
    except Exception as e:
        print(f"Lỗi chèn dữ liệu: {e}")
        traceback.print_exc()
    else:
        print(f"Thêm dữ liệu tự động vào Bang_{table}_Kho thành công")
        cursor.commit()

def add_data_tree_f2():
    # Tạo cửa sổ thêm dữ liệu
    add_win = tk.Toplevel()
    add_win.title("Thêm dữ liệu")
    add_win.geometry('300x200+600+550')
    global conn
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time = str(current_time)
    # data=tuple(data)
    # data = data + (time,)
    # Tạo các trường nhập liệu
    can_close = tk.BooleanVar()
    check_box = tk.Checkbutton(add_win, text="Giữ cửa sổ", variable=can_close).grid(row=8,column=8)

    id_entrylb = tk.Label(add_win, text='Mã hàng').grid(row=0, column=0)
    id_entry = tk.Entry(add_win)
    id_entry.grid(row=0, column=1)
    
    name_entrylb = tk.Label(add_win, text='Tên hàng')
    name_entrylb.grid(row=1, column=0)
    name_entry = tk.Entry(add_win)
    name_entry.grid(row=1, column=1)
    
    source_entrylb = tk.Label(add_win, text='Xuất xứ')
    source_entrylb.grid(row=2, column=0)
    source_entry = tk.Entry(add_win)
    source_entry.grid(row=2, column=1)
    
    ##############################
    price_in_entrylb = tk.Label(add_win, text='Giá nhập')
    price_in_entrylb.grid(row=3, column=0)
    price_in_entry = tk.Entry(add_win)
    price_in_entry.grid(row=3, column=1)
    
    price_out_entrylb = tk.Label(add_win, text='Giá xuất')
    price_out_entrylb.grid(row=4, column=0)
    price_out_entry = tk.Entry(add_win)
    price_out_entry.grid(row=4, column=1)

    tk.Label(add_win, text='Số lượng').grid(row=5, column=0)
    quantity_entry = tk.Entry(add_win)
    quantity_entry.grid(row=5, column=1)
    
    locate_entrylb = tk.Label(add_win, text='Khu vực')
    locate_entrylb.grid(row=6, column=0)
    locate_entry = tk.Entry(add_win)
    locate_entry.grid(row=6, column=1)
    if nameTableData.get() in ("Nhap","Xuat"):
        name_entry.grid_forget()
        locate_entry.grid_forget()
        price_in_entry.grid_forget()
        price_out_entry.grid_forget()
        source_entry.grid_forget()

        name_entrylb.grid_forget()
        locate_entrylb.grid_forget()
        price_in_entrylb.grid_forget()
        price_out_entrylb.grid_forget()
        source_entrylb.grid_forget()
    # Nút thêm dữ liệu
    def save_data():
        # Lấy dữ liệu từ các trường nhập liệu
        new_values = ()
        sql_query = ""
        soluong = int(quantity_entry.get())
        if nameTableData.get() in ("Nhap","Xuat"):
            new_values = selectData_dataBase(id_entry.get())
            if(nameTableData.get() == "Xuat" and (new_values[5] < soluong) ):
                messagebox.showinfo("Thông báo",f"Không đủ hàng trong kho, còn lại: {new_values[5]}")
            else:   
                sql_query = f"INSERT INTO Bang_{nameTableData.get()}_Kho (MaHang,TenHang,XuatXu,GiaNhap,GiaBan,SoLuong{nameTableData.get()},KhuVuc,ThoiGian{nameTableData.get()}) VALUES (?,?,?,?,?,?,?,?)"      
                new_values=tuple(new_values)
                new_values = new_values + (time,)
                new_values = new_values[:5] + (soluong,) + new_values[5 + 1:]
                print(new_values)
                add_dataBase_to_TreeView(new_values,nameTableData.get())
        else:
            new_values = (id_entry.get(), name_entry.get(), source_entry.get(),price_in_entry.get(),price_out_entry.get(),soluong,locate_entry.get())
            sql_query = "INSERT INTO Bang_Tong_Kho (MaHang,TenHang,XuatXu,GiaNhap,GiaBan,SoLuongKho,KhuVuc) VALUES (?,?,?,?,?,?,?)"      
        # Thêm dữ liệu vào Treeview
        # table.insert('', 'end', values=new_values)
        new_values=tuple(new_values)
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query,new_values)
        except Exception as e:
            print(f"Lỗi chèn dữ liệu: {e}")
            traceback.print_exc()
        else:
            print(f"Thêm thủ công dữ liệu vào Bang_{nameTableData.get()}_Kho thành công")
        cursor.commit()
        # Đóng cửa sổ thêm dữ liệu

        if not can_close.get():
            add_win.destroy()
        else: 
            pass
            
    
    tk.Button(add_win, text='Thêm', command=save_data).grid(row=7, columnspan=2) 

dem = 1
btThemData_Tong = tk.Button(frame2,
                       text='Thêm dữ liệu tổng kho',
                       command=add_data_tree_f2
                       )
btThemData_Tong.place(x=120,y=700)
def reset_counter_lastData():
    global dem 
    dem =1
    global last_data
    last_data = ''
    if nameTableData.get() == "Nhap":
        btThemData_Tong.config(text='Nhập dữ liệu thủ công')
    elif nameTableData.get() == "Xuat":
        btThemData_Tong.config(text='Xuất dữ liệu thủ công')
    else:
        btThemData_Tong.config(text='Thêm dữ liệu tổng kho')

def ThaoTac():
    nameTable.config(text="Bảng thao tác")
    table.delete(*table.get_children())
    colum_ThaoTac = ("0","1","2")
    table.config(columns=colum_ThaoTac)
    table.heading("#0", text="STT")
    table.heading("0", text="Name")
    table.heading("1", text="Trạng thái")
    table.heading("2", text="Thời gian")
    # table.heading("3", text="Ca làm")
    # table.heading("4", text="Người làm")
    table.column("#0", width=150)
    # table.column("6", width=150)
    table.pack(fill="both", padx=0, pady=350)

    counter =1
    sql_query = f"SELECT _NAME,_VALUE,_TIMESTAMP FROM [dbo].[Bang_Thao_Tac]"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        # Lấy tất cả các dòng từ kết quả truy vấn
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Lỗi lấy dữ liệu: {e}")
        traceback.print_exc()
    else:
        if rows:
        # Chuyển đổi dữ liệu thành list các dòng và gán vào biến
            data_select = [list(row) for row in rows]
            # print('Truy vấn dữ liệu thành công')
    name_mapping = {
    "Channel1.Device1.Tags.Tag1": " Vat A",
    "Channel1.Device1.Tags.Tag2": " Vat B",
    "Channel1.Device1.Tags.Tag3": " Vat C",
    "Channel1.Device1.Tags.Tag4": " Vat D",
    "Channel1.Device1.Tags.Tag5": "CB Reset A",
    "Channel1.Device1.Tags.Tag6": "CB Reset B"        ,
    "Channel1.Device1.Tags.Tag7": "CB Reset C"        ,
    "Channel1.Device1.Tags.Tag8": "CB Reset D"        ,
    # "Channel1.Device1.Tags.Tag9": "Vat A"        ,
    # "Channel1.Device1.Tags.Tag10": "Vat B"        ,
    # "Channel1.Device1.Tags.Tag11": "Vat C"        ,
    # "Channel1.Device1.Tags.Tag12": "Vat D"        ,
    # "Channel1.Device1.Tags.Tag13": "Start"        ,
    "Channel1.Device1.Tags.Tag14": "CB Xilanh"        ,
    "Channel1.Device1.Tags.Tag15": "CTHT DC1 N"        ,


    }      
    for row in data_select:
    # Lấy giá trị của cột _NAME trong dòng hiện tại
        name_value = row[0]
        
        # Thực hiện thay đổi tên
        if name_value in name_mapping:
        # Nếu có, thay đổi giá trị cũ thành giá trị mới từ từ điển
            row[0] = name_mapping[name_value]
    for i in range(len(data_select)):
        # print(data_select[i][0])
        table.insert("", "end", text=str(counter), values=data_select[i])
        counter+=1
        if counter == len(data_select) +1:
            counter=1

    # Đặt biến kiểm tra trạng thái
    should_continue = True

    # Kiểm tra điều kiện
    if nameTableData.get() == "Thao_Tac":
        root.after(100, ThaoTac)
    else:
        # Gán biến kiểm tra trạng thái là False nếu điều kiện không được thỏa mãn
        root.after_cancel()

    # Dừng việc gọi root.after nếu biến kiểm tra trạng thái là False



    last_item = table.get_children()[-1]
    # table.selection_set(last_item)
    # Cuộn xuống dòng cuối cùng
    table.see(last_item)


def nhapKho():
    setup_table("Bảng nhập kho", "Thời gian nhập")
    reset_counter_lastData()
def xuatKho():
    setup_table("Bảng xuất kho", "Thời gian xuất")
    reset_counter_lastData()
def tongKho():
    counter =1
    setup_table("Bảng tổng kho")
    reset_counter_lastData()
    sql_query = f"SELECT * FROM Bang_Tong_Kho"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        # Lấy tất cả các dòng từ kết quả truy vấn
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Lỗi lấy dữ liệu: {e}")
        traceback.print_exc()
    else:
        if rows:
        # Chuyển đổi dữ liệu thành list các dòng và gán vào biến
            data_select = [list(row) for row in rows]
            # print('Truy vấn dữ liệu thành công')
    
    
    # print(data_select[0][0])
    for i in range(len(data_select)):
        table.insert("", "end", text=str(counter), values=data_select[i])
        counter+=1
        if counter == len(data_select) +1 :
            counter=1

nameTableData.set("Tong")
if nameTableData.get() == "Tong":
    tongKho()
    print("helolo")
    
#RadioButton NhapKho
r = ttk.Radiobutton(
        frame2,
        text="Nhập kho",
        value="Nhap",
        variable=nameTableData,
        command=nhapKho
    ).place(x=20,y=550)
#RadioButton XuatKho
r1 = ttk.Radiobutton(
        frame2,
        text="Xuất kho",
        value="Xuat",
        variable=nameTableData,
        command=xuatKho
    ).place(x=20,y=600)
#RadioButton TongKho
r2 = ttk.Radiobutton(
        frame2,
        text="Tổng kho",
        value="Tong",
        variable=nameTableData,
        command=tongKho
    ).place(x=20,y=650)
r3 = ttk.Radiobutton(
        frame2,
        text="Thao tác",
        value="Thao_Tac",
        variable=nameTableData,
        command=ThaoTac
    ).place(x=150,y=650) 


##############################################################################################################################
# dem = 1
def add_dataBase_to_TreeView(data,tablename):
    # global counter
    global dem
    # global nameTableData
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    time = str(current_time)
    # data=list(data.split(","))
    data=tuple(data)
    data = data + (time,)
    # print(data)
    print(type(tablename))
    table.insert("", "end", text=str(dem), values=data)
    # # table.insert("", "end", text=str(counter), values=(f"Nội dung ", current_time))
    last_item = table.get_children()[-1]
    # table.selection_set(last_item)
    # Cuộn xuống dòng cuối cùng
    table.see(last_item)
    dem = dem + 1
time_start_total = ()
time_end_total = ()
addWin=""

def KiemTraXuatEx():
    if nameTableData.get() == "Tong":
        sql_query = " SELECT * FROM Bang_Tong_Kho"
        ExportElxs(sql_query)
    else:
        luaChonThoiGianXuatEx()

def luaChonThoiGianXuatEx():
    global addWin
    addWin = tk.Toplevel()
    addWin.title("Lựa chọn thời gian xuất dữ liệu")
    addWin.geometry('300x120+600+550')
    global time_end_total,time_start_total
    global conn
    nam_lb = tk.Label(addWin,text="Năm").grid(row=0,column=2)
    thang_lb = tk.Label(addWin,text="Tháng").grid(row=0,column=3)
    ngay_lb = tk.Label(addWin,text="Ngày").grid(row=0,column=4)
    gio_lb = tk.Label(addWin,text="Giờ").grid(row=0,column=5)
    phut_lb = tk.Label(addWin,text="Phút").grid(row=0,column=6)

    time_start_lb = tk.Label(addWin,text="Từ: ").grid(row=1,column=1)
    time_start_nam = tk.Entry(addWin,width=5)
    time_start_nam.grid(row=1,column=2)
    time_start_thang = tk.Entry(addWin,width=5)
    time_start_thang.grid(row=1,column=3)
    time_start_ngay = tk.Entry(addWin,width=5)
    time_start_ngay.grid(row=1,column=4)
    time_start_gio = tk.Entry(addWin,width=5)
    time_start_gio.grid(row=1,column=5)
    time_start_phut = tk.Entry(addWin,width=5)
    time_start_phut.grid(row=1,column=6)


    time_end_lb = tk.Label(addWin,text="Đến: ").grid(row=2,column=1)
    time_end_nam = tk.Entry(addWin,width=5)
    time_end_nam.grid(row=2,column=2) 
    time_end_thang = tk.Entry(addWin,width=5)
    time_end_thang.grid(row=2,column=3)
    time_end_ngay = tk.Entry(addWin,width=5)
    time_end_ngay.grid(row=2,column=4)
    time_end_gio = tk.Entry(addWin,width=5)
    time_end_gio.grid(row=2,column=5)
    time_end_phut = tk.Entry(addWin,width=5)
    time_end_phut.grid(row=2,column=6)
    
# Biến để lưu trạng thái của checkbutton
    
    ckb_xuattoanbo_var = tk.IntVar()
    # lb_xuattoanbo = tk.Label(addWin,text="Xuất toàn bộ dữ liệu").place(x=100,y=65)
    ckb_xuattoanbo = tk.Checkbutton(addWin,text="Xuất toàn bộ dữ liệu", variable=ckb_xuattoanbo_var)
    ckb_xuattoanbo.place(x=100,y=65)   

    
   



    def save_data():
        # time_start_total = ()
        # time_end_total = ()
        global time_end_total,time_start_total
        global nameTable
        time_start_total = (time_start_nam.get(),time_start_thang.get(),time_start_ngay.get(),time_start_gio.get(),time_start_phut.get())
        time_end_total   = (time_end_nam.get(),time_end_thang.get(),time_end_ngay.get(),time_end_gio.get(),time_end_phut.get())
        
        print(time_start_total)
        print(time_end_total)

        time_toltal = (time_start_total,time_end_total)
        # if time_toltal:
        #     print(time_toltal)
        #     print("khong rong")
        name_table = str(nameTableData.get())
        if name_table == "Xuat":
            name_table = "Bang_Xuat_Kho"
        elif name_table == "Nhap":
            name_table = "Bang_Nhap_Kho"
        elif name_table == "Tong":
            name_table = "Bang_Tong_Kho"
        elif name_table == "Thao_Tac":
            name_table == "Bang_Thao_Tac"

        if nameTableData.get() in ("Nhap","Xuat") and ckb_xuattoanbo_var.get() == 0:
            sql_query = f'''
            SELECT MaHang, TenHang, XuatXu, GiaNhap, GiaBan, KhuVuc, SUM(SoLuong{nameTableData.get()}) AS TongSoLuong{nameTableData.get()}
            FROM Bang_{nameTableData.get()}_Kho
            WHERE ThoiGian{nameTableData.get()} BETWEEN '{time_start_nam.get()}-{time_start_thang.get()}-{time_start_ngay.get()} {time_start_gio.get()}:{time_start_phut.get()}' AND '{time_end_nam.get()}-{time_end_thang.get()}-{time_end_ngay.get()} {time_end_gio.get()}:{time_end_phut.get()}'
            GROUP BY MaHang, TenHang, XuatXu, GiaNhap, GiaBan, KhuVuc;
            '''
        elif nameTableData.get() == "Thao_Tac" and ckb_xuattoanbo_var.get() == 0:
            sql_query = f'''
            SELECT _NAME AS TEN,_VALUE AS GiaTri, COUNT(_VALUE) AS TongThaoTac
            FROM Bang_Thao_Tac
            WHERE _TIMESTAMP BETWEEN '{time_start_nam.get()}-{time_start_thang.get()}-{time_start_ngay.get()} {time_start_gio.get()}:{time_start_phut.get()}' AND '{time_end_nam.get()}-{time_end_thang.get()}-{time_end_ngay.get()} {time_end_gio.get()}:{time_end_phut.get()}'
            GROUP BY _NAME,_VALUE;
            '''
            print(sql_query)
        elif ckb_xuattoanbo_var.get() == 1:
            sql_query = f"SELECT * FROM {name_table}"
            print(sql_query)

        else:
            print("Checkbutton không được chọn")
        addWin.destroy()
        ExportElxs(sql_query)
        # file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])

    
    tk.Button(addWin, text='Thêm', command=save_data).place(x=50,y=80)
    


def ExportElxs(sql_query):
    global conn
    global nameTableData
    global addWin
    
    # kq = pd.read_sql(f'SELECT * FROM {name_table}',conn)
    try:
            # Thực hiện truy vấn SQL và tạo DataFrame từ kết quả
        df = pd.read_sql(sql_query, conn)
        # Tạo một từ điển ánh xạ giữa các tên cũ và tên mới
        if nameTableData.get() == "Thao_Tac":
            name_mapping = {
                "Channel1.Device1.Tags.Tag1": " Vat A",
                "Channel1.Device1.Tags.Tag2": " Vat B",
                "Channel1.Device1.Tags.Tag3": " Vat C",
                "Channel1.Device1.Tags.Tag4": " Vat D",
                "Channel1.Device1.Tags.Tag5": "CB Reset A",
                "Cannel1.Device1.Tags.Tag7": "CB Reset C"        ,
                "Chahannel1.Device1.Tags.Tag6": "CB Reset B"        ,
                "Chnnel1.Device1.Tags.Tag8": "CB Reset D"        ,
                "Channel1.Device1.Tags.Tag9": "Vat A"        ,
                "Channel1.Device1.Tags.Tag10": "Vat B"        ,
                "Channel1.Device1.Tags.Tag11": "Vat C"        ,
                "Channel1.Device1.Tags.Tag12": "Vat D"        ,
                "Channel1.Device1.Tags.Tag13": "Start"        ,
                "Channel1.Device1.Tags.Tag14": "CB Xilanh"        ,
                "Channel1.Device1.Tags.Tag15": "CTHT DC1 N"        ,


                # Thêm các ánh xạ khác nếu cần thiết
            }

            # Thực hiện thay đổi tên cột
            df.rename(columns={'TEN': 'Ten'}, inplace=True)

            # Thay đổi tên của các cột dựa trên từ điển ánh xạ
            df['Ten'] = df['Ten'].map(name_mapping).fillna(df['Ten'])

        print(df)
        dfr = pd.DataFrame(df)
        
    except Exception as e:
        print("Có lỗi xảy ra khi thực hiện truy vấn SQL:", e)
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])
    # Nếu người dùng chọn một đường dẫn, thực hiện việc xuất Excel
    if file_path:
        print(f"file_path{file_path}")
        dfr.to_excel(file_path,index=False)


def on_btXuatExcel():
    excel = threading.Thread(target=KiemTraXuatEx)
    excel.start()

btXuatExcel = tk.Button(
    master=frame2,
    text='Xuất file excel',
    command=on_btXuatExcel                   
    ).place(x=10,y=700)
def HienThiThongBaoHetHang():
    messagebox.showinfo("Thông báo",f"Không đủ hàng trong kho còn lại: 0")
def thongBao_HetHang():
    loi = threading.Thread(target=HienThiThongBaoHetHang)
    loi.start()



def delete_data():
    # Lấy id của hàng được chọn
    selected_item = table.focus()
    if selected_item:
        confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa dữ liệu đã chọn?")
        if confirm:
            sql_query = f"DELETE FROM Bang_{nameTableData.get()}_Kho WHERE MaHang = {get_selected_data_from_tree()[0]}"      
            # Thêm dữ liệu vào Treeview
            # table.insert('', 'end', values=new_values)
            try:
                cursor = conn.cursor()
                cursor.execute(sql_query)
            except Exception as e:
                print(f"Lỗi chèn dữ liệu: {e}")
                traceback.print_exc()
            else:
                print(f"Xóa dữ liệu trong Bang_{nameTableData.get()}_Kho thành công")
            cursor.commit() 

            table.delete(selected_item)
    else:
        messagebox.showinfo("Thông báo","Bạn chưa chọn dữ liệu")
def get_selected_data_from_tree():
    selected_item = table.selection()  # Lấy item được chọn
    if selected_item:  # Kiểm tra xem có hàng nào được chọn không
        item = table.item(selected_item)
        values = item['values']
        print("Dữ liệu được chọn:", values)
        # print(values[0])
        # print(selectData_dataBase(values[0]))
        new_values = selectData_dataBase(values[0])
    else:
        # print("Không có hàng nào được chọn.")
        messagebox.showinfo("Thông báo","Không có hàng nào được chọn.") 
    return new_values
delete_button = tk.Button(frame2, text='Xóa dữ liệu', command=delete_data)
delete_button.place(x=280,y=700)

update_button = tk.Button(frame2, text='Sửa dữ liệu', command="")
update_button.place(x=380,y=700)
def truyenThongArd(data_frame):
 # Tạo từ điển ánh xạ giữa data_frame và chuỗi cần gửi
    data_mapping = {
        '001': '1',
        '002': '2',
        '003': '3',
        '004': '4',
        '005': '5',
        '006': '6',
        '007': '7',
        '008': '8'
    }

    # Kiểm tra xem data_frame có trong từ điển không
    if data_frame in data_mapping:
        # Gửi chuỗi tương ứng với data_frame
        Arduino_Serial.write(data_mapping[data_frame].encode())
    else:
        myOutput = 'Khong trong kho'


def capturedVideo():
    global handle_frame_img
    global data, last_data
    global conn, directionOfQrCode
    global nameTableData
    global ktratable
    MaHang= list()
    # data_frame = list()
    status,frame = camera.read()
    if status == False:
        message = messagebox.showerror("Lỗi","Camera của bay bị hỏng à")
        sys.exit()
    else:
        rgb_type_arr = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        info = decode(rgb_type_arr)
        #Nếu trong info có Class Decode được tạo thì sẽ lấy dữ liệu
        if len(info)>0:
            DecodedObject = info[0]
            # print(DecodedObject)
            GeometryOfQrCode = DecodedObject.polygon
            #--Hướng của mã QR Code dựa trên 3 đỉnh
            # có 4 trường hợp:
            # 1 .LEFT, 2. RIGHT, 3. UP, 4. DOWN
            directionOfQrCode = DecodedObject.orientation
            dimensionofQrCode = DecodedObject.rect
            # print(directionOfQrCode)
            # print(DirectionOfQrCode)
            #Vẽ đa giác ABCD bằng tọa độ các đỉnh
            point_A = [GeometryOfQrCode[0].x,GeometryOfQrCode[0].y]
            point_B = [GeometryOfQrCode[1].x,GeometryOfQrCode[1].y]
            point_C = [GeometryOfQrCode[2].x,GeometryOfQrCode[2].y]
            point_D = [GeometryOfQrCode[3].x,GeometryOfQrCode[3].y]
            
            pts = np.array([point_A,point_B,point_C,point_D],dtype=np.int32)
            #Mỗi không gian chứa 2 điểm, do đó cần reshape
            pts = pts.reshape((-1,1,2))
            #Vẽ đa giác trên frame
            frame_drew = cv.polylines(rgb_type_arr,[pts],True,color=(0,255,0),thickness=2)
            # print(point_C)
            # print(point_D)
            #Vị trí chữ dựa trên chiều của mã QR
            point_text1 = (int(point_C[0]-((dimensionofQrCode.width)/1)),int(point_C[1]-80))
            point_text2 = (int(point_C[0]-((dimensionofQrCode.width)/1)),int(point_C[1]-30))
            # print(point_text1)
            #Lấy dữ liệu, chuyển dữ liệu gốc về dạng UTF-8
            data = DecodedObject.data.decode('utf-8')
            data_frame = list(data.split(","))
            data_frame = list(data_frame)
            df = pd.read_sql('SELECT * FROM Bang_Tong_Kho',conn)
            if data_frame[0] in df['MaHang'].values:
                frame_text1 = cv.putText(frame_drew,text=f'Ma:{data_frame[0]}',fontFace=cv.FONT_HERSHEY_PLAIN,fontScale=3,color=(0,255,0),org=point_text1,thickness=2)
                frame_text2 = cv.putText(frame_drew,text='In Stock',fontFace=cv.FONT_HERSHEY_PLAIN,fontScale=3,color=(0,255,0),org=point_text2,thickness=2)
                if last_data != data_frame[0]:
                    #Biến lưu giá trị truy vấn từ CSDL
                    data_temp = selectData_dataBase(data_frame[0]) # là một tuple
                    data_ktra = data_temp
                    data_temp = data_temp[:5] + (1,) + data_temp[5 + 1:] 
                    name_table = str(nameTableData.get()) #Biến lấy giá trị tên của bảng cần chèn
                    if(nameTableData.get() == "Xuat" and (data_ktra[5] == 0 ) ):
                        thongBao_HetHang()
                    elif name_table in ("Nhap","Xuat"):
                        # truyenThongArd(data_frame[0])  #- sử dụng khi có arduino
                        insertData(data_temp,name_table)
                        add_dataBase_to_TreeView(data_temp,name_table)
                    last_data = data_frame[0]    

            else:
                frame_text1 = cv.putText(frame_drew,text=f'Ma:{data_frame[0]}',fontFace=cv.FONT_HERSHEY_PLAIN,fontScale=3,color=(255,0,0),org=point_text1,thickness=2)
                frame_text2 = cv.putText(frame_drew,text='Out of Stock',fontFace=cv.FONT_HERSHEY_PLAIN,fontScale=3,color=(255,0,0),org=point_text2,thickness=2)

            image = Image.fromarray(frame_text1)
            image = image.resize((600,400))
            destImage = ImageTk.PhotoImage(image=image)
            handle_frame_img.configure(
                image=destImage
            )
            handle_frame_img.image = destImage
                #Loop after 20ms
            handle_frame_img.place(x=0,y=400)
            handle_frame_img.after(20,capturedVideo)
        else:
            image = Image.fromarray(rgb_type_arr)
            image = image.resize((600,400))
            destImage = ImageTk.PhotoImage(image=image)
            handle_frame_img.configure(
                image=destImage
            )
            handle_frame_img.image = destImage
                #Loop after 20ms
            handle_frame_img.place(x=0,y=400)
            handle_frame_img.after(20,capturedVideo)
capturedVideo()
root.mainloop()
camera.release()


       
