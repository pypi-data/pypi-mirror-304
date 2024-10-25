**Make PIP your self**

1. `git clone https://github.com/humblesami/djform_navigation.git`
2. `cd djform_navigation`

3. Find and replace `djform_navigation` with your own `your_module_name`

**Build and test using sample_usage locally**

rm -r dist/*

rm -r build/*

pip install -r requirements.txt

python setup.py sdist bdist_wheel -v=1.1

**Test the built package**

`pip uninstall -y djform_navigation`

`pip install dist/djform_navigation-1.1-py3-none-any.whl`

`cd sample_usage`

`python manage.py initsql`

`python manage.py runserver`

open https://127.0.0.1:8000/admin/ 

username `sa`

password `123`

Open model1

**Upload your pip**

Install twine

`sudo apt-get update`

`sudo apt-get install twine`

https://twine.readthedocs.io/en/stable/

`pip install twine`

**Sample config files for twine**

1. .pypirc_test (add this to root directory where setup.py exists)

    [distutils]
    index-servers = pypi

    [pypi]
    repository: https://test.pypi.org/legacy/
    username: __token__
    password: token1


2. .pypirc_prod (add this to root directory where setup.py exists)

    [distutils]
    index-servers = pypi

    [pypi]
    repository: https://pypi.org/legacy/
    username: __token__
    password: token2

**Final Step**

`twine upload dist/* --config-file .pypirc_test`

*After upload Install the uploaded package*

pip install -i https://test.pypi.org/simple/ djform_navigation


`twine upload dist/* --config-file .pypirc_prod`

*After upload Install the uploaded package*

pip install djform_navigation