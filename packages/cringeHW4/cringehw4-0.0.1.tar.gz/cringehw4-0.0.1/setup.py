from setuptools import setup


setup(
    name='cringeHW4',
    version='0.0.1',
    py_modules=["order_receipt"],  # Модули, которые вы хотите включить
    entry_points={
        'console_scripts': [
            'order-receipt=order_receipt:main',  # Команда для запуска скрипта
        ],
    },
    author= 'osisochka',
    author_email= 'a.onufrienko@edu.centraluniversity.ru',
    description='generation of ordered receipts',
    python_requires='>=3.6',
)

