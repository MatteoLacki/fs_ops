net use M: \\msserver\majestix_rawdata
python C:/Projects/fs_ops/bin/msync.py D:/Data/raw M:/RAW "*.d" --min_copy_hours 1 --min_delete_hours 48 --debug --server_ip_port 192.168.1.100:9002
pause