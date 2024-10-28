from setuptools import setup, find_packages

setup(
    name="tsk_2", 
    version="0.1.1",
    description="Пакет для анализа финансовых транзакций",
    author="bardachell", 
    author_email="jenda-penda@mail.ru", 
    packages=find_packages(), 
    install_requires=["setuptools", "wheel"], 
    entry_points={
        'console_scripts': [
            'tsk_2 = task_2.transaction_counter:main',
        ],
    },
    python_requires='>=3.7', 
)