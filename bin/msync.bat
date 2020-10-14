net use M: \\msserver\majestix_rawdata
python C:/Projects/fs_ops/bin/msync.py D:/Data/raw M:/RAW "*.d" --min_copy_hours 4 --min_delete_hours 48 --debug
pause