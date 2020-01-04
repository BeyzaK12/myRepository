------------------------------------------------------------------------------------------------------------------------
Mobile Price Classification Using KNN
------------------------------------------------------------------------------------------------------------------------

INSTRUCTIONS FOR RUNNING THE PROGRAM
1- Run 'knn.py' (python3 knn.py)
2- Enter 'k' value

'knn.py' finds Euclidean distances between every phones in the 'test.txt' file and every phones in the 'train.txt' file.
Then, it finds the accuracy of price ranges of phones in 'test.txt' with using the KNN classification.
If k value is less than 10, the program calculates the accuracies of all cases where k is between 0 and 11.
If k value is more than 10, the program calculates the accuracies of all cases where k is between 0 and k value.
While calculating accuracy values, it puts values to a list.
At the same time, when it finds k's accuracy, it prints the accuracy to the terminal.
Finally, it creates a bar plot with k values and their accuracies.

---------------------------------------------------
TERMINAL EXAMPLE
---------------------------------------------------
beyza@beyzak12:~/ceng3511/p4$ python3 knn.py
k: 5
acc: 0.9170829170829171
[(1, 0.8991008991008991), (2, 0.8821178821178821), (3, 0.9070929070929071), (4, 0.9120879120879121), (5, 0.9170829170829171), (6, 0.919080919080919), (7, 0.9240759240759241), (8, 0.922077922077922), (9, 0.9240759240759241), (10, 0.922077922077922)]

***The plot was written to the 'plot.pdf' file.***
---------------------------------------------------

-The pdf file of this terminal example is in repo.
