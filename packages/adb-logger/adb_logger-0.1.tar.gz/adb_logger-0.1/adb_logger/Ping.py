import subprocess


def ping_ip(ip):
    """
    Send a ping request to the specified IP address and return the result.
    """
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", ip])
        return True
    except subprocess.CalledProcessError:
        return False
