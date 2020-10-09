make:
	echo "hello"
test_pip:
	twine -r test blablabla
update_pip:
	twine blablabla
test_files:
	mkdir -p tests/A.d/ha.m
	mkdir -p tests/B.d/ha.m
	touch tests/A.d/a.tdf
	touch tests/A.d/a.tdf_bin
	touch tests/A.d/ha.m/method
	touch tests/B.d/a.tdf
	touch tests/B.d/a.tdf_bin
	touch tests/B.d/ha.m/method
	touch tests/V1.raw
	touch tests/V2.raw
clean_tests:
	rm -rf tests
copy_bruker:
	msync.py /home/matteo/Projects/fs_ops/tests /home/matteo/Projects/fs_ops/res *.d --min_copy_hours .001 --debug
copy_thermo:
	msync.py /home/matteo/Projects/fs_ops/tests /home/matteo/Projects/fs_ops/res *.raw --min_copy_hours .001 --debug
copy_bruker_win:
	python C:/Projects/fs_ops/bin/msync.py C:/Projects/fs_ops/tests C:/Projects/fs_ops/res *.d --min_copy_hours .001 --debug
copy_thermo_win:
	python C:/Projects/fs_ops/bin/msync.py C:/Projects/fs_ops/tests C:/Projects/fs_ops/res *.raw --min_copy_hours .001	--debug
ipython:
	python -m IPython
install:
	pip uninstall -y fs_ops || True
	pip install -e .
