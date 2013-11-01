'''
Created on Jun 18, 2013

@author: ivan
'''

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace
import remote

import logging
log=logging.getLogger('mp.sockets')
#TODO: Move remote init to server start
remote.init(True)


@namespace('/log')
class LogController(BaseNamespace):
    def initialize(self):
        log.debug('Log Controller started')
        
    def on_start(self, stream_id):
        log.debug('Started %s', stream_id)
        ctx=remote.context()
        socket=remote.create_socket(ctx, 'sub')
        try:
            remote.sub_msg(socket, stream_id.encode('utf-8'))
            def on_msg(proc_id, mtype, msg):
                print "##MSG", mtype,msg
                self.emit(mtype, msg)
                if mtype=='done':
                    self.disconnect()
                    return True
            try:
                remote.poll_msg(socket, on_msg)
            except remote.TimeoutError:
                print "##TIMEOUT"
                log.warn('SUB socket timeout')
                self.disconnect()
        finally:
            socket.close()
            
        print "##END"
        