# Example Package

This is a simple example package. You can use
[GitHub-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

python -m pip install --upgrade build
python -m build
python -m twine upload --cert C:\works\packaging_tutorial\.venv\Lib\site-packages\cibcert\certs\cibcabundle.crt dist/*
python -m pip install --upgrade twine
