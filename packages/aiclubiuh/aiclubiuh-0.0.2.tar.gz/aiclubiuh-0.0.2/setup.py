from setuptools import setup, find_packages
# rmdir /s /q dist 
# python setup.py sdist bdist_wheel
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# twine upload --repository-url https://test.pypi.org/legacy/ -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkZGJlZDY4ZjgtMDcyNS00YjY3LTk2YWEtY2YzMTJhMGI2YmUyAAIqWzMsIjk3NTJjOGQxLTQ1NjMtNGE5OC1hMzQxLWEzYWEzZmRkYTc4NyJdAAAGIIiu5bYz0n46bTnbatEfjq5WNIJtPDuCHxWzrK3ehgtB dist/*
# twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGYxM2U2NGRjLWFjZGMtNDJiMy1hNDQ0LTUzZTlhMDU2YTk1ZgACKlszLCJkNDE2ODQyOS04YmM4LTRkNzEtODIxNS00MjhlNDg5Yjc3MjEiXQAABiA7GI7Ucun-naBBF63xgaweTVW3W8R9YVk5JiYYe4sdjg dist/*
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='aiclubiuh',
    version='0.0.2',
    packages=find_packages(),
    description='Thư viện hỗ trợ cho AI Club IUH',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='htanh',
    author_email='anhkhdl@gmail.com',
    url="https://main.aiclubiuh.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "rich"  # Thêm dòng này để tự động cài đặt rich
    ],
)
