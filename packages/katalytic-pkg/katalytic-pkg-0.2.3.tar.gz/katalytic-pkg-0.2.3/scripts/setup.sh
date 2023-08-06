# reset
source scripts/cleanup.sh
~/anaconda3/envs/py36/bin/python -m venv venv
source venv/bin/activate

# install deps
python -m pip install --upgrade pip
python -m pip install --upgrade $(python scripts/find_requirements.py)

# install this pkg
if [[ $1 == 'pypi' ]]; then
	python -m pip install $(cdir)
elif [[ $1 == 'test' ]]; then
	python -m pip install -i https://test.pypi.org/simple/ $(cdir)
else
	python -m pip install -e .
fi

# test
source scripts/pytest.sh
