import subprocess
import re
from pprint import pp

class FSMonitoring():
    ''' This class provides a serie of methos to allow Filesystem monitoring.
        
        CLASS ATTRIBUTES:
        =================
        
         - filesystem: LIST of filesystems to be checked. If only one: ['/fs'].
         - disk_treshold: treshold for disk limit. Default: 80%.
         - inode_treshold: treshold for inodes limit. Default: 80%.
         - disk_usage_label: This label with differ between linux distros.
                             Log in your target host and execute df command to look for the correct one.
                             Default: 'Use%'.
         - inodes_usage_label: This label with differ between linux distros.
                               Log in your target host and execute df command to look for the correct one.
                               Default: 'IUse%'.
    '''

    def __init__(self, filesystem, disk_treshold = 80, inode_treshold = 80,
                   disk_usage_label = 'Use%' , inodes_usage_label = 'IUse%'):
        self.filesystem = filesystem
        self.disk_treshold = disk_treshold
        self.inode_treshold = inode_treshold
        self.disk_usage_label = disk_usage_label
        self.inodes_usage_label = inodes_usage_label
        self.result = []

    def __getiem__(self, i):
        return self.result[i]
    
    def parse_stdout(self, sp_return):
        '''
            Parses 'subprocess.CompletedProcess' stdout into a dictionary

            e.g.:

            sp_return.stdout =
            Filesystem                           Size  Used Avail Use% Mounted on
            /dev/mapper/example                   99G  5.5G   93G   6% /opt/example

            returned value:
            {
            'Filesystem': '/dev/mapper/example',
            'Size': '99G',
            'Used': '5.5G',
            'Avail': '93G',
            'Use%': '6%',
            'Mounted': '/opt/example'
            }  
        '''
        sp_stdout = sp_return.stdout.decode("utf-8")
        list_sp_stdout = sp_stdout.rstrip("\n").split('\n')
        return dict(zip(list_sp_stdout[0].split(),list_sp_stdout[1].split()))
    
    def get_fs_usage(self, check_disk = True, check_inodes = False):
        '''
            Execute LOCALLY "df" command and return a list of dictionaries with the usage of each
            filesystem.
            Also manage the following exceptions:
                - Filesystem not found.
                - filesystem name TypeError.
                    e.g.:
                         self.filesystem = 1
        '''
        for fs in self.filesystem:
            try:
                if check_inodes:
                    sp_return = subprocess.run(["df","-khi", fs],capture_output=True, check=True)
                    self.result.append(self.parse_stdout(sp_return))
                if check_disk:
                    sp_return = subprocess.run(["df","-kh", fs],capture_output=True, check=True) 
                    self.result.append(self.parse_stdout(sp_return))
            except subprocess.CalledProcessError as e:
                self.result.append(f'ERROR: Filsystem not found. Stdout: {e}')
            except TypeError as e:
                self.result.append(f'TYPEERROR: Malformed file system name: {fs}')
        return self.result
    
    def get_percentage_usage(self, result):
        '''return % usage of a filesystem (inodes or disk)'''
        if type(result) is dict:
            if self.disk_usage_label in result :
                return 'disk', result['Mounted'], int(re.findall(r'[0-9]{1,3}', result[self.disk_usage_label])[0])
            if self.inodes_usage_label in result:
                return 'inodes', result['Mounted'], int(re.findall(r'[0-9]{1,3}', result[self.inodes_usage_label])[0])
        return None, None, result
    
    def get_directories_size(filesystem):
        '''
            This function gets a "filesystem path" and returns:
                - Size used
                - A dictionary with all subdirectories within the same filesystem and its size
                (different filesystems within the primary filesystem are excluded).

                e.g.:
                filesystem = /tmp/test
                total_size = 1G
                dir_info = {
                    'tmp/test/2' = '700M',
                    'tmp/test/1' = '300M',
                    'tmp/test' = '1G',
                    'total' = '1G'
                    }
                    
        '''
        try:
            sp_return = subprocess.run(["du","-chx", filesystem],capture_output=True, check=True)
            sp_stdout = sp_return.stdout.decode("utf-8")
            directories = sp_stdout.rstrip("\n").split('\n')
            dirs_names = []
            dirs_sizes = []
            for i in directories:
                size, name = i.split()
                dirs_names.append(name)
                dirs_sizes.append(size)
            dir_info = dict(zip(dirs_names, dirs_sizes))
            total_size = dir_info['total']
            return [dir_info, total_size]
        except subprocess.CalledProcessError:
            print(e)
            return None

    def write_logs(self, filename):
        '''
            Write logs about file system information.

            Logs format:
            
                OK: /var/atlassian disk usage is 1 percent and the treshold is set to 80 percent
                OK: /var/atlassian inodes usage is 1 percent and the treshold is set to 80 percent
                TYPEERROR: Malformed file system name: 1
                WARNING: /dev disk usage has exceeded 80 percent
                WARNING: /dev inodes usage has exceeded 80 percent
                ERROR: Filsystem not found. Stdout: Command '['df', '-khi', '/test']' returned non-zero exit status 1.
                
        '''
        with open(filename, 'w') as f:
            for r in range(len(self.result)):
                info_type, fs_name, perc_usage = self.get_percentage_usage(self.result[r])
                if info_type == 'disk':
                    if perc_usage < self.disk_treshold:
                        f.write(f'OK: {fs_name} {info_type} usage is {perc_usage} percent and the treshold is set to {self.disk_treshold} percent\n')
                    else:
                        f.write(f'WARNING: {fs_name} {info_type} usage has exceeded {self.disk_treshold} percent \n')
                elif info_type == 'inodes':        
                    if perc_usage < self.inode_treshold:
                        f.write(f'OK: {fs_name} {info_type} usage is {perc_usage} percent and the treshold is set to {self.inode_treshold} percent\n')
                    else:
                        f.write(f'WARNING: {fs_name} {info_type} usage has exceeded {self.inode_treshold} percent \n')
                else:
                    f.write(f'{self.result[r]}\n')

if __name__ == "__main__":
 
    fs_monitoring = FSMonitoring([1, "/test" ,"/dev", "/var/atlassian"],
                                 disk_treshold = 1,
                                 disk_usage_label = 'Use%',
                                 inodes_usage_label = 'IUse%')
    result = fs_monitoring.get_fs_usage(check_inodes = True)
    fs_monitoring.write_logs('fs_monitoring.log')

    
            

