import subprocess
import time
import os


def start_logcat(final_ip_list):
    for x in final_ip_list:
        # Add the path to the adb command to the PATH environment variable(Used for testing since my adb can be buggy but it should work fine without it)
        #os.environ["PATH"] += os.pathsep + "/Users/chowja4/Library/Android/sdk/platform-tools"
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        if x:
            # Start logcat for a specific IP address and direct output to file
            logcat_file = f"logcat_{x}_{timestamp}.txt"
            cmd = ["adb", "-s", f"{x}", "logcat", "-v", "time", "-f", logcat_file]

        else:
            # Start default logcat and direct output to file
            logcat_file = f"logcat_{timestamp}.txt"
            cmd = ["adb", "logcat", "-v", "time", "-f", logcat_file]

        # Start logcat process
        process = subprocess.Popen(cmd)


        #TODO Change hardcoded open area to implementation like Terminal.py Tends to hang and you can't interact with gui
        with open(f'/Users/{logcat_file}', 'a') as f:
            if x:
                subprocess.run(['adb', '-s', f'{x}', 'logcat', '-v', 'time'], stdout=f)
            else:
                subprocess.run(['adb', 'logcat', '-v', 'time'], stdout=f)


            process.communicate(timeout=15)
            #TODO
            process.kill()
            process.communicate()

        # with open(logcat_file, "r") as f:
        #     logcat_output = f.read()
        #     print(logcat_output)

    return 0