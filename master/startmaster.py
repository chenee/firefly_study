#coding:utf8

import os
if os.name != 'nt' and os.name != 'posix':
    from twisted.internet import epollreactor
    epollreactor.install()

if __name__ == "__main__":
    from master import Master
    master = Master('config.json')
    master.startMaster()

    # master.startChildren()
