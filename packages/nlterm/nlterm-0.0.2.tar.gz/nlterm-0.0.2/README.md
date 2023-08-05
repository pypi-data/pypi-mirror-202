# `nlterm`: Integrate ChatGPT in your terminal

# Install
```
pip install nlterm
```

# Example

````
> nlterm
Instruction: reorgnize this folder to like a pypi project. That is I need to put scripts in `src` folder, and have a basic `pyproject.toml`
````
This is the output:
````
```
mkdir src
mv *.py src
touch pyproject.toml
```
Execute? (y/n): y
````