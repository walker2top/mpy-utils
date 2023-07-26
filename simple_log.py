import time

__LEVELS = ['ERROR', 'WARN', 'INFO', 'DEBUG']
__RED = '\033[31m'
__DEFAULT = '\033[38m'
__YELLOW = '\033[33m'
__GREEN = '\033[32m'
__COLOR_CODE = {'ERROR': __RED, 'INFO': __DEFAULT, 'WARN':__YELLOW,'DEBUG':__GREEN}

class Log:
    
    def __init__(self,):
        self.min_level = 'DEBUG'
    
    def set_min_level(level: str):
        if level not in __LEVELS:
            raise ValueError('{level} is not supported as log levels: {__LEVELS}!')
        self.min_level = level
        
    def console_log(self, log_level, *args):
        if __LEVELS.index(log_level) > __LEVELS.index(self.min_level):
            return
        
        def zfill(src:str, width: int):
            src = str(src)
            distance = width-len(src)
            if distance>0:
                src = '0'* distance + src
            return src
        
        current = time.localtime()
        content = ''.join([str(item) for item in args])
        log_line=f'[{zfill(current[0],4)}-{zfill(current[1],2)}-{zfill(current[2],2)} {zfill(current[3],2)}:{zfill(current[4],2)}:{zfill(current[5],2)}] [{log_level}] - {content}'
        log_line = __COLOR_CODE.get(log_level, __DEFAULT)+log_line+"\033[0m"
        print(log_line)
        
    def info(self, *args):
        self.console_log('INFO', *args)
    
    def error(self, *args):
        self.console_log('ERROR', *args)
    
    def debug(self, *args):
        self.console_log('DEBUG', *args)
    
    def warn(self, *args):
        self.console_log('WARN', *args)
        

log = Log()