#!/bin/sh

echo
echo '[VERSION AT src/cochl_sense_api/__init__.py]'
grep __version__ src/cochl_sense_api/__init__.py

echo

echo '[VERSION AT pyproject.toml]'
grep version pyproject.toml
echo

echo 'Do versions match? (y/n)'
read -r ANSWER

echo "${ANSWER}"

if [ "${ANSWER}" = "n" ]; then
  exit
fi

sudo apt install python3.8
sudo apt install python3.8-venv

python3.8 --version
python3.8 -m pip install --upgrade pip
python3.8 -m pip install --upgrade build

rm -rf dist
mkdir dist
rm -rf .gitignore

python3.8 -m build
git reset --hard

python3.8 -m pip install --upgrade twine

cp -f ~/.test_pypirc ~/.pypirc
python3.8 -m twine upload dist/* --verbose --repository testpypi
rm -rf ~/.pypirc
