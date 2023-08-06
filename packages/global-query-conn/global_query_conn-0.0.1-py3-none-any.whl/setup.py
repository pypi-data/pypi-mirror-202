from setuptools import setup

setup(
    name='global_query_conn',
    version='0.0.1',    
    description='Query package untuk postgresql terlebih dahulu',
    url='https://github.com/shuds13/pyexample',
    author='Arief Prabowo',
    author_email='',
    license='BSD 2-clause',
    packages=['global_query_conn'],
    install_requires=['psycopg2-binary==2.9.5',
                      'pymongo==4.3.3',
                      'mysql-connector-python==8.0.32'                     
                      ],
)