This repository contains scripts for  automatically check file-systems usage.

The report is written in a log file.

# Tested on:

- MacOS Catalina V.10.15.7
- CSOE V.7.7 

# Prerequisites:

- Python 3.9
- Python modules:
    - subprocess
    - re 

# How to use it?

- Import the module in your own Python script.
```python
# script name: my_monitoring_script.py 
from fs_monitoring import FSMonitoring

fs_monitoring = FSMonitoring([1, "/test" ,"/dev", "/var/atlassian"],
                                 disk_usage_label = 'Capacity', # Mac users
                                 inodes_usage_label = 'IUsed%') # Mac users
result = fs_monitoring.get_fs_usage(check_inodes = True)
fs_monitoring.write_logs('test.log')
```

- Execute it
```bash
python3.9 my_monitoring_script.py 
```
- Check your log file:
```bash
cat test.log
```

# How would your log file look?

```            
TYPEERROR: Malformed file system name: 1
ERROR: Filsystem not found. Stdout: Command '['df', '-khi', '/test']' returned non-zero exit status 1.
WARNING: /dev disk usage has exceeded 80 percent
WARNING: /dev inodes usage has exceeded 80 percent
OK: /var/atlassian disk usage is 1 percent and the treshold is set to 80 percent
OK: /var/atlassian inodes usage is 1 percent and the treshold is set to 80 percent
```

# Module Doc:

```python
>>> from fs_monitoring import FSMonitoring
>>> help(FSMonitoring)
Help on class FSMonitoring in module __main__:

class FSMonitoring(builtins.object)
 |  FSMonitoring(filesystem, disk_treshold=80, inode_treshold=80, disk_usage_label='Use%', inodes_usage_label='IUse%')
 |  
 |  This class provides a serie of methos to allow Filesystem monitoring.
 |  
 |  CLASS ATTRIBUTES:
 |  =================
 |  
 |   - filesystem: LIST of filesystems to be checked. If only one: ['/fs'].
 |   - disk_treshold: treshold for disk limit. Default: 80%.
 |   - inode_treshold: treshold for inodes limit. Default: 80%.
 |   - disk_usage_label: This label with differ between linux distros.
 |                       Log in your target host and execute df command to look for the correct one.
 |                       Default: 'Use%'.
 |   - inodes_usage_label: This label with differ between linux distros.
 |                         Log in your target host and execute df command to look for the correct one.
 |                         Default: 'IUse%'.
 |  
 |  Methods defined here:
 |  
 |  __getiem__(self, i)
 |  
 |  __init__(self, filesystem, disk_treshold=80, inode_treshold=80, disk_usage_label='Use%', inodes_usage_label='IUse%')
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  get_directories_size(filesystem)
 |      This function gets a "filesystem path" and returns:
 |          - Size used
 |          - A dictionary with all subdirectories within the same filesystem and its size
 |          (different filesystems within the primary filesystem are excluded).
 |      
 |          e.g.:
 |          filesystem = /tmp/test
 |          total_size = 1G
 |          dir_info = {
 |              'tmp/test/2' = '700M',
 |              'tmp/test/1' = '300M',
 |              'tmp/test' = '1G',
 |              'total' = '1G'
 |              }
 |  
 |  get_fs_usage(self, check_disk=True, check_inodes=False)
 |      Execute LOCALLY "df" command and return a list of dictionaries with the usage of each
 |      filesystem.
 |      Also manage the following exceptions:
 |          - Filesystem not found.
 |          - filesystem name TYPEERROR.
 |              e.g.:
 |                   self.filesystem = 1
 |  
 |  get_percentage_usage(self, result)
 |      return % usage of a filesystem (inodes or disk)
 |  
 |  parse_stdout(self, sp_return)
 |      Parses 'subprocess.CompletedProcess' stdout into a dictionary
 |      
 |      e.g.:
 |      
 |      sp_return.stdout =
 |      Filesystem                           Size  Used Avail Use% Mounted on
 |      /dev/mapper/example                   99G  5.5G   93G   6% /opt/example
 |      
 |      returned value:
 |      {
 |      'Filesystem': '/dev/mapper/example',
 |      'Size': '99G',
 |      'Used': '5.5G',
 |      'Avail': '93G',
 |      'Use%': '6%',
 |      'Mounted': '/opt/example'
 |      }
 |  
 |  write_logs(self, filename)
 |      Write logs about file system information.
 |      
 |      Logs format:
 |      
 |          OK: /var/atlassian disk usage is 1 percent and the treshold is set to 80 percent
 |          OK: /var/atlassian inodes usage is 1 percent and the treshold is set to 80 percent
 |          TYPEERROR: Malformed file system name: 1
 |          WARNING: /dev disk usage has exceeded 80 percent
 |          WARNING: /dev inodes usage has exceeded 80 percent
 |          ERROR: Filsystem not found. Stdout: Command '['df', '-khi', '/test']' returned non-zero exit status 1.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 ```
