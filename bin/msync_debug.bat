rem python C:/Projects/fs_ops/bin/msync.py C:/Projects/fs_ops/tests C:/Projects/fs_ops/res *.d --min_copy_hours .001 --debug
rem python C:/Projects/fs_ops/bin/msync.py D:/Data/raw_test_msync M:/test_sync *.d --min_copy_hours .001 --min_delete_hours 48 --debug
rem python C:/Projects/fs_ops/bin/msync.py D:/Data/raw M:/raw *.d --min_copy_hours 4 --min_delete_hours 48 --debug
net use M: \\msserver\majestix_rawdata
python C:/Projects/fs_ops/bin/msync.py D:/Data/raw M:/test_sync2 "F2020-09-10_16-15-39_Training2_57.d" --min_copy_hours 4 --min_delete_hours 48 --debug
pause