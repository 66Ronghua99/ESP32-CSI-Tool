import subprocess
import pty
import os
import time
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p","--port")
parser.add_argument("-o", "--output")
args = parser.parse_args()

# process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

master, slave = pty.openpty()

# 定义要执行的命令
command = f"sourceidf; idf.py monitor -p {args.port}"

# 使用 subprocess.Popen 来执行命令，指定伪终端的 slave 作为 stdin 和 stdout
process = subprocess.Popen(command, shell=True, stdin=slave, stdout=slave, stderr=subprocess.STDOUT, close_fds=True)

# 打开一个文件用于写入输出
try:
    with open(args.output, 'w') as file:
        print("Open file")
        # 使用循环来读取输出
        while True:
            try:
                line = os.read(master, 1024)
                line_decoded = line.decode(errors="replace")
            except OSError:
                break  # 如果读取失败（例如进程结束），则退出循环
            except UnicodeDecodeError:
                line_decoded = line.decode('ISO-8859-1', errors='replace')
                # 如果解码失败，尝试使用ISO-8859-1编码
            print(line_decoded)
            if "CSI_DATA" not in line_decoded:
                continue
            # 将输出行写入文件
            if "len" in line_decoded:
                line_decoded = "time," + line_decoded
            else:
                line_decoded = str(time.time()) + "," + line_decoded
            file.write(line_decoded)
            # 同时在控制台打印输出
            print(line_decoded, end='')
        print("No output")

except KeyboardInterrupt:
    # 如果用户按下Ctrl+C，终止进程
    print("\nTerminating process...")
    os.write(master, b'\x1d')
    print("Process terminated.")