import datetime

SUCCESS = 'SUCCESS'
ERROR = 'ERROR'
WARNING = 'WARNING'

log_file = '../log(%s).log'

def _log(info, level):
    print info
    now = datetime.datetime.now()
    with open(log_file % now.strftime("%Y-%m-%d"), 'a+') as f:
        f.write('%s %s %s\n' % (level, now.strftime("%Y-%m-%d %H:%M:%S"), info))


if __name__ == '__main__':
    _log('haha', SUCCESS)

