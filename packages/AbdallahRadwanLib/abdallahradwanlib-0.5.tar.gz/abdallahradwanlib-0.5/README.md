# AbdallahPackage
* Install the following packages : 
    pip install twine
    pip install setuptools wheel
    pip install tqdm
    python setup.py sdist
    twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

* Update My Package :    
    Update the Version Number
    clear setup info
        rm -rf dist/ build/ *.egg-info
    
    prepare setup info 
        python setup.py bdist_wheel
        python setup.py sdist
                or
        python setup.py bdist_wheel sdist

    twine check dist/*    
    
    twine upload dist/*
            or
    twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

    past my token

    pip install dist/AbdallahRadwanLib-0.4-py3-none-any.whl
    
    

* Reinstall with --force-reinstall and --no-binary
    pip install --force-reinstall --no-binary=:all: AbdallahRadwanLib

* Download the source manually
    pip download --no-binary=:all: AbdallahRadwanLib
    tar -xvzf AbdallahRadwanLib-0.4.tar.gz


* View at:
    https://pypi.org/project/AbdallahRadwanLib/0.4/

* Install Command :
    pip install AbdallahRadwanLib==0.4


    