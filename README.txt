-- WHAT THIS DOES --
Takes an uploaded csv file, and generates a databse for it, while
outputting the DDL. It will create the populated 'db' file and a
complementary sql file with it.

-- HOW TO USE IT --
Install all modules required
1) Run 'main.py
2) On your web browser, go to 'localhost:5000' (or whatever port)
3) Press the 'choose file' button and select mock_data.csv 
4) Press 'submit'
5) A db/sql file will be created, and the DDL will be outputted.
   You can choose to clear the output box or copy the DDL.