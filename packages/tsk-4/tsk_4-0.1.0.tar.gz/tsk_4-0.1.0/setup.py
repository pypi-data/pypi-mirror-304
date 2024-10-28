from setuptools import setup, find_packages

setup(
    name="tsk_4", 
    version="0.1.0",
    description="Generate Reciept",
    author="bardachell", 
    author_email="jenda-penda@mail.ru", 
    packages=find_packages(), 
    install_requires=["setuptools", "wheel"], 
    entry_points={
        'console_scripts': [
            'tsk_4 = task_4.generate_reciept:main',
        ],
    },
    python_requires='>=3.7', 
)