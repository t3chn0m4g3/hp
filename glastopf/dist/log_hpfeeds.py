# Copyright (C) 2015 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import logging
import os
import base64
import gevent
import hpfeeds
from glastopf.modules.reporting.auxiliary.base_logger import BaseLogger


logger = logging.getLogger(__name__)


class HPFeedsLogger(BaseLogger):

    def __init__(self, data_dir, work_dir, config="glastopf.cfg", reconnect=True):
        config = os.path.join(work_dir, config)
        BaseLogger.__init__(self, config)
        self.files_dir = os.path.join(data_dir, 'files/')
        self.enabled = False
        self._initial_connection_happend = False
        #legacy
        self.options = {'enabled': self.enabled}
        if self.config.getboolean("hpfeed", "enabled"):
            host = os.environ['GLASTOPF_HPFEEDS_HOST']
            port = os.environ['GLASTOPF_HPFEEDS_PORT']
            ident = os.environ['GLASTOPF_HPFEEDS_IDENT']
            secret = os.environ['GLASTOPF_HPFEEDS_SECRET']
            self.enabled = True
            #legacy
            self.options = {'enabled': self.enabled}
            self.chan_files = os.environ['GLASTOPF_HPFEEDS_FILES']
            self.chan_events = os.environ['GLASTOPF_HPFEEDS_EVENTS']
            self.hpc = None
            gevent.spawn(self._start_connection, host, port, ident, secret, reconnect)

    def _start_connection(self, host, port, ident, secret, reconnect):
            # if no initial connection to hpfeeds this will hang forever, reconnect=True only comes into play
            # when lost connection after the initial connect happend.
            self.hpc = hpfeeds.new(host, port, ident, secret, reconnect)
            self._initial_connection_happend = True

    def insert(self, attack_event):
        if self._initial_connection_happend:
            if attack_event.file_name is not None:
                with file(os.path.join(self.files_dir, attack_event.file_name), 'r') as file_handler:
                    logger.debug('Sending file ({0}) using hpfriends on {0}'.format(attack_event.file_name, self.chan_files))
                    file_content = file_handler.read()
                    file_data = attack_event.file_name + " " + base64.b64encode(file_content)
                    self.hpc.publish(self.chan_files, file_data)

            event_data = json.dumps(attack_event.event_dict())
            self.hpc.publish(self.chan_events, event_data)
        else:
            logger.warning('Not logging event because initial hpfeeds connect has not happend yet')
