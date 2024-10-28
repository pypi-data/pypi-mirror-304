from setuptools import setup, find_packages

setup(
    name="tsk_3", 
    version="0.1.0",
    description="Sales Report",
    author="bardachell", 
    author_email="jenda-penda@mail.ru", 
    packages=find_packages(), 
    install_requires=["setuptools", "wheel"], 
    entry_points={
        'console_scripts': [
            'tsk_3 = task_3.sales_report:main',
        ],
    },
    python_requires='>=3.7', 
)