make:
	echo "hello"
test_pip:
	twine -r test blablabla
update_pip:
	twine blablabla
test_lib:
	mkdir -p tests/A
	mkdir -p tests/B
	mkdir -p tests/res
	mkdir -p tests/A/C
	touch tests/A/C/c
	touch tests/A/a
	touch tests/A/a0
	touch tests/A/a1
	touch tests/B/b
clean_tests:
	rm -rf tests
ipython:
	python -m IPython
