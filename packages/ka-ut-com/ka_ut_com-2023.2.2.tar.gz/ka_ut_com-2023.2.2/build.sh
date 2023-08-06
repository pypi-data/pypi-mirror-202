pip3 install black!=23.1.0

black --check ./ka_ut_com
pipreqs --force --ignore .mypy_cache --mode gt .
mypy ./ka_ut_com

ruff --clean 
ruff --fix ./ka_ut_com

pip3 install .

cd /app/ka_com/ka_ut_com/docs; make man

python3 -m build --wheel --sdist
twine check dist/*
twine upload dist/*
