CENG 3511
Artificial Intelligence
Project 2: Solving CSPs

Beyza KURT
160709017

This project includes two Python codes to solve the Kakuro and Futoshiki puzzles.
In addition, there are 2 input files where we can see the given values of the puzzles.

⚫ kakuros.py
-------------
  link: https://i.hizliresim.com/Z5qJJ3.png
  answer: https://i.hizliresim.com/Lv6EQa.png

  kakuro_input.txt (sample input file):
  22, 18, 7
  20, 19, 8

  To execute Python code:
  ----------------------
  -Enter the "p2" folder to execute the code.
  -Type "python3 kakuros.py" at the terminal.
  -The code is not going to print anything.
  -When the files in the folder are listed, the file "kakuro_output.txt" appears.

  kakuro_output.txt (sample output file):
  x, 22, 18, 7
  20, 9, 7, 4
  19, 8, 9, 2
  8, 5, 2, 1

  The nxn kakuro puzzle using this code is cannot solved.
  Even if what is n is known from the input file, it is not assigned as variable name
  because it will be read from the file as a string.
  The nxn kakuro puzzle is cannot solved without variable names.

⚫ futoshiki.py
---------------
  link: https://i.hizliresim.com/lQD9EB.png
  answer: https://i.hizliresim.com/bv0YMj.png

  futoshiki_input.txt (sample input file):
  B2, 1
  D4, 2
  A1, A2
  A4, B4
  C2, C1
  D2, C2

  To execute Python code:
  ----------------------
  -Enter the "p2" folder to execute the code.
  -Type "python3 futoshiki.py" at the terminal.
  -The code is not going to print anything.
  -When the files in the folder are listed, the file "futoshiki_output.txt" appears.

  futoshiki_output.txt (sample output file):
  3, 2, 1, 4
  4, 1, 2, 3
  2, 3, 4, 1
  1, 4, 3, 2

  The nxn futoshiki puzzle is cannot solved with this input file.
  If the n is given in the input file, the code can be modified to solve the puzzle.
