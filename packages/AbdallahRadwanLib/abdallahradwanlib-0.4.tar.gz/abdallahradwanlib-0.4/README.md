# AbdallahPackage

pip install twine
pip install setuptools wheel
pip install tqdm
python setup.py sdist
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

* Update My Package :
    
Update the Version Number
rm -rf dist/ build/ *.egg-info
python setup.py sdist bdist_wheel
pip install dist/AbdallahRadwanLib-0.4-py3-none-any.whl   
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
past my token


* View at:
    https://pypi.org/project/AbdallahRadwanLib/0.1/
    https://pypi.org/project/AbdallahRadwanLib/0.2/
    https://pypi.org/project/AbdallahRadwanLib/0.3/

* Install Command :
    pip install AbdallahRadwanLib==0.1


    