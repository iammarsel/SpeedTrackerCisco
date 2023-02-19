from tkinter import *
from netmiko import ConnectHandler
from customtkinter import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

set_appearance_mode("System")
set_default_color_theme("green")

window = CTk()
window.title("Speed Tracking Application")
window.geometry("700x500")

ios_l2 = {
    'device_type': 'cisco_ios',
    'username': '',
    'ip': '',
    'password': '',
    'conn_timeout': 9999999
}

pause = False
index = 0
toggle_text = "Pause"
font = {'family': 'Times New Roman',
        'weight': 'bold',
        'size': 22
        }
matplotlib.rc('font', **font)


def onChange():
    global pause
    pause ^= True
    if pause:
        pause_button.configure(
            text="Continue", fg_color="#119149", hover_color="#45ba78")
    else:
        pause_button.configure(
            text="Pause", fg_color="#c74c3c", hover_color="#9c2b1c")


def onStart():
    ios_l2['ip'] = device_ip.get()
    ios_l2['username'] = device_username.get()
    ios_l2['password'] = device_password.get()
    ssh = ConnectHandler(**ios_l2)
    try:
        plt.style.use('dark_background')
        plt.title("Speed Tracking for Device")
        plt.xlabel('Time')
        plt.ylabel('Speed (mb/s)')
        ax = plt.gca()
        plt.grid()
        ax.set_facecolor('#cccccc')

        input_speeds = []
        output_speeds = []
        times = []

        global pause_button

        pause_button = CTkButton(
            window, text="Pause", command=onChange, fg_color="#c74c3c", hover_color="#9c2b1c")
        pause_button.place(relx=0.5, rely=0.8, anchor=CENTER)

        def animate(i):
            if not pause:
                getspeed = ssh.send_command(f"sh int g0/1/3 | i rate")
                getspeed = getspeed.split("\n")
                current_input = getspeed[1].split()
                current_output = getspeed[2].split()
                global index
                index += 1
                times.append(index)
                if len(input_speeds) > 1:
                    input_speeds.append(input_speeds[-1])
                    output_speeds.append(output_speeds[-1])
                    times.append(index)
                input_speeds.append(int(current_input[4])/1000000)
                output_speeds.append(int(current_output[4])/1000000)
                plt.cla()
                plt.title("Speed Tracking for Device")
                plt.xlabel('Time (seconds)')
                plt.ylabel('Speed (Mb/s)')
                plt.plot(times, input_speeds, label="Input Speed", color="red")
                plt.plot(times, output_speeds,
                         label="Output Speed", color="blue")
                plt.grid()
                plt.legend(loc="lower right")
                if index > 60:
                    plt.xlim(left=index-60)
                else:
                    plt.xlim(0, 60)
                plt.ylim(0, max(max(input_speeds), max(output_speeds))*1.2)

        ani = FuncAnimation(plt.gcf(), animate, interval=1000)

        plt.show()

    except KeyboardInterrupt:
        print('Interrupted by user')
    except:
        print('error found at', device_ip)


greeting = CTkLabel(window, text="Load Device and Track Speed using Graph")
greeting.place(relx=0.5, rely=0.1, anchor=CENTER)


device_ip = CTkEntry(window, placeholder_text="IP Address",
                     width=120,
                     height=25,
                     border_width=2,
                     corner_radius=10)
device_ip.place(relx=0.5, rely=0.2, anchor=CENTER)

device_username = CTkEntry(window, placeholder_text="Username",
                           width=120,
                           height=25,
                           border_width=2,
                           corner_radius=10)
device_username.place(relx=0.5, rely=0.3, anchor=CENTER)
device_password = CTkEntry(window, placeholder_text="Password",
                           width=120,
                           height=25,
                           border_width=2,
                           corner_radius=10)
device_password.place(relx=0.5, rely=0.4, anchor=CENTER)
device_port = CTkEntry(window, placeholder_text="Port Number",
                       width=120,
                       height=25,
                       border_width=2,
                       corner_radius=10)
device_port.place(relx=0.5, rely=0.5, anchor=CENTER)


load_button = CTkButton(window, text="Start", command=onStart,
                        fg_color="#119149", hover_color="#45ba78")
load_button.place(relx=0.5, rely=0.7, anchor=CENTER)
window.mainloop()
