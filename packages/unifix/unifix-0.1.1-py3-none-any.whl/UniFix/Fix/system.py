'''
system info
'''
import platform


def info():
    '''
    get system info
    '''
    return f"""
        OS Name     : {platform.system()}
        OS Version  : {platform.release()}
        OS Arch     : {platform.machine()}
    """


if __name__ == "__main__":
    print(info())
