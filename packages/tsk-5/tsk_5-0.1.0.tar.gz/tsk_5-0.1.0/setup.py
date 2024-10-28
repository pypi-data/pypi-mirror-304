from setuptools import setup, find_packages

setup(
    name="tsk_5", 
    version="0.1.0",
    description="Customer Analysis",
    author="bardachell", 
    author_email="jenda-penda@mail.ru", 
    packages=find_packages(), 
    install_requires=["setuptools", "wheel"], 
    entry_points={
        'console_scripts': [
            'tsk_5 = task_5.customer_analysis:main',
        ],
    },
    python_requires='>=3.7', 
)