pip3 install black!=23.1.0

black --check ./ks_ut_gen
pipreqs --force --ignore .mypy_cache --mode gt .
mypy ./ks_ut_gen

ruff --clean 
ruff --fix ./ks_ut_gen

pip3 install .

cd /app/ks_ut_gen/ks_ut_gen/docs; make man

python3 -m build --wheel --sdist
twine check dist/*
twine upload dist/*
