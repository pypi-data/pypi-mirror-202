pip3 install black!=23.1.0

black --check ./ka_ut_obj
pipreqs --force --ignore .mypy_cache --mode gt .
mypy ./ka_ut_obj

ruff --clean 
ruff --fix ./ka_ut_obj

pip3 install .

cd /app/ka_ut_obj/ka_ut_obj/docs; make man

python3 -m build --wheel --sdist
twine check dist/*
twine upload dist/*
