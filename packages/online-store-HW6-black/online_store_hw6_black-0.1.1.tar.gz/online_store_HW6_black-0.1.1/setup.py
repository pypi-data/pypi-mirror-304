from setuptools import setup, find_packages

setup(
    name="online_store_HW6_black", 
    version="0.1.1", 
    description="Исполняемый пакет для управления пользователями и заказами в онлайн-магазине", 
    author="bardachell", 
    author_email="jenda-penda@mail.ru", 
    packages=find_packages(),  
    install_requires=["requests", "flask", "sqlalchemy", "marshmallow"], 
    entry_points={
        'console_scripts': [
            'online_store_HW6_black = online_store.files.main:main',  
        ],
    },
    python_requires='>=3.7', 
)