# Project 6: Brevet time calculator service

Same base as project 6, but added different extensions to list data from the database in different formats.

## Extensions

/listAll/csv

- list all of the open and close times in a csv format

/listAll/json

- list all of the open and close times in a json format

/listOpenOnly/csv

- list only the open times in a csv format

/listOpenOnly/json

- list only the open times in a json format

/listOpenOnly/csv?top=k

- list only the top k open times in a csv format

/listOpenOnly/json?top=k

- list only the top k open times in a json format

/listCloseOnly/csv

- list only the close times in a csv format

/listCloseOnly/json

- list only the close times in a json format

/listCloseOnly/csv?top=k

- list only the top k close times in a csv format

/listCloseOnly/json?top=k

- list only the top k close times in a json format


# Usage

1. Create a MongoDB database (I used mLab)
2. Create a collection in that database called "times"
3. Create a credentials.ini based on credentials-skel.ini
4. Run everything with "docker-compose up"
6. Fill up calculator (http://<host>:<port>/)
7. Submit to your database ("Submit" button on bottom of page)
8. Get the format you want! (http://<host>:<port>/<extension>/)
