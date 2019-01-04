#!/bin/sh

# install runtime
cd pkgs

# install python3.6
tar zxvf Python-3.6.8.tgz
cd Python-3.6.8
./configure --prefix=/usr/local/python3.6
make
make install
ln -s /usr/local/python3.6/bin/python3.6 /usr/local/bin/python3
ln -s /usr/local/python3.6/bin/pip3 /usr/local/bin/pip3
cd ..
rm -rf Python-3.6.8

# install wheel
tar zxvf wheel-0.32.3.tar.gz
cd wheel-0.32.3
python3 setup.py install
cd ..
rm -rf wheel-0.32.3

# install dependency
pip3 install numpy-1.14.5-cp36-cp36m-manylinux1_x86_64.whl
pip3 install six-1.12.0-py2.py3-none-any.whl
pip3 install python_dateutil-2.7.5-py2.py3-none-any.whl
pip3 install pytz-2018.7-py2.py3-none-any.whl
pip3 install pandas-0.22.0-cp36-cp36m-manylinux1_x86_64.whl
pip3 install scipy-1.2.0-cp36-cp36m-manylinux1_x86_64.whl
pip3 install scikit_learn-0.19.2-cp36-cp36m-manylinux1_x86_64.whl

# install outliers
cd ..
python3 setup.py build
python3 setup.py install
ln -s /usr/local/python3.6/bin/outliers /usr/local/bin/outliers
