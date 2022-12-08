install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C --extension-pkg-whitelist='pydantic' /10_code/*.ipynb

format:
	black /10_code/*.ipynb

all: install lint format
