from toddy import puts,logs

show_logs = False

def show_console(arg):
    global show_logs
    show_logs = arg

def log(*ipts,sep=' ',filepath='logs.txt',save=False):
    if show_logs:
        puts(*ipts,pathfile=filepath,save=save,sep=sep)
    else:
        pass
