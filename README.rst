******************
ppcwiz - submitter
******************

How to run this program?
########################

1. Create a virtual environment of your choice inside the directory and install all the dependencies from the **requirements.txt** file:
::
  pip install -r requirements.txt


2. Running the **main.py** file is enough to start the program:
:: 
  python main.py

Additional libraries used in the project
########################################

1. SQLAlchemy - Object Relational Mapper (ORM)
**********************************************

* Full documentation of the libary can be found `here <https://docs.sqlalchemy.org/en/14/>`_

2. Alembic - a migration tool
*****************************

* To create migrations:
  ::
    alembic revision --autogenerate -m "some message"

* To migrate:
  :: 
    alembic upgrade head


* Full documentation of the library can be found `here <https://alembic.sqlalchemy.org/en/latest/>`_
