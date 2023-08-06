import subprocess
import time


def terminal_connect(num_of_ip, final_ip_list):
    # Add the path to the adb command to the PATH environment variable(Used for testing since my adb can be buggy on the computer Im using but it should work fine without it)
    # os.environ["PATH"] += os.pathsep + "/Users/chowja4/Library/Android/sdk/platform-tools"
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    adb_commands = []
    filename = []
    # Makes a List of Adb Commands to send
    for x in range(num_of_ip):
        adb_commands.append(f'adb -s {final_ip_list[x]} logcat > logcat{x}_{final_ip_list[x]}_{timestamp}.txt')
        filename.append(f'logcat{x}_{final_ip_list[x]}_{timestamp}.txt')

    y = 0
    for command in adb_commands:
        subprocess.call(['open', '-n', '-g', '-a', 'Terminal'])
        # time.sleep(1)
        subprocess.call(['osascript', '-e', f'tell application "Terminal" to do script "{command}" in window {y}'])
        y = y + 1


    return filename
