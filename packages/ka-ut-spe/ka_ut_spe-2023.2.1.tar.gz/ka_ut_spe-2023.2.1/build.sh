pip3 install black!=23.1.0

black --check ./ka_ut_spe
pipreqs --force --ignore .mypy_cache --mode gt .
mypy ./ka_ut_spe

ruff --clean
ruff --fix ./ka_ut_spe

pip3 install .

cd /app/ka_ut_spe/ka_ut_spe/docs; make man

python3 -m build --wheel --sdist
twine check dist/*
twine upload dist/*
