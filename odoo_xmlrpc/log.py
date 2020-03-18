import datetime

SUCCESS = 'SUCCESS'
ERROR = 'ERROR'
WARNING = 'WARNING'

log_file = '../log(%s).log'

def _log(info, level=SUCCESS):
    print(info)
    now = datetime.datetime.now()
    f_name = log_file % now.strftime("%Y-%m-%d")
    with open(f_name, 'a+') as f:
        f.write('%s %s %s\n' % (level, now.strftime("%Y-%m-%d %H:%M:%S"), info))


if __name__ == '__main__':
    _log('haha', SUCCESS)

