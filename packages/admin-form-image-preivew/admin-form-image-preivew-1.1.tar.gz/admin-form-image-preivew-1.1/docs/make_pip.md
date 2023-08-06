**Make PIP your self**

Open containing folder of this file
cd ../

rm -r dist/*
rm -r build/*
python setup.py clean --all
python setup.py sdist bdist_wheel -v=1.1

**Install and test locally**
pip uninstall admin-form-image-preivew
pip install dist/admin_form_image_preivew-1.0-py3-none-any.whl


**Upload your**

https://twine.readthedocs.io/en/stable/

pip install twine

twine upload dist/*
twine upload dist/* --config-file ~/.pypirc1
or
twine upload dist/* --config-file ~/.pypirc2


**Sample config files for twine**

1.
.pypirc1

[distutils]
index-servers = pypi

[pypi]
repository: https://test.pypi.org/legacy/
username: __token__
password: token1



*Install the uploaded package*
pip install -i https://test.pypi.org/simple/ admin-form-image-preivew

================================================================

2.
.pypirc2

[distutils]
index-servers = pypi

[pypi]
repository: https://pypi.org/legacy/
username: __token__
password: token2

*Install the uploaded package*
pip install admin-form-image-preivew