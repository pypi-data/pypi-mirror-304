# Argument Components - Identification and Classification
## structure
- command_line.py is the entry point for the module. from here the user should be able to run training and inference.
- ./inference/ is the directory that houses everything inference related
- ./training/ is the directory that houses everything training related
## update
when prompted, use `__token__` for the username and the api key including the pypi- prefix 
```
enva
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```
## install - for testing 
```
python3 -m pip install --upgrade --index-url https://test.pypi.org/simple/ --no-deps AC-IaC
```
