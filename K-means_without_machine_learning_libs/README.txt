------------------------------------------------------------------------------------------------------------------------
K-means In Action
------------------------------------------------------------------------------------------------------------------------

INSTRUCTIONS FOR RUNNING THE PROGRAM
1- Run 'kmeans.py' (python3 kmeans.py)
2- Enter 'the number of centers' value

- Receives the number of centers from the user as input
- Reads points coordinates from 'data.txt' file
1. Selects K (the number of centers) random points as cluster centers called centroids
2. Assigns each data point to the closest cluster by calculating its distance with respect to each centroid
3. Determines the new cluster center by computing the average of the assigned points
4. Repeats steps 2 and 3 until none of the cluster assignments change
- Gives centroid's coordinates and theirs clusters' point numbers in the terminal
- Creates a plot with using 'matplotlib'
- Saves the plot as pdf file; 'plot.pdf'


---------------------------------------------------
TERMINAL EXAMPLE
---------------------------------------------------
beyza@beyzak12:~/ceng3511/p5$ python3 kmeans.py
The number of centers: 5

1. centroid is  [320, 151]
The number of points in its cluster: 52

2. centroid is  [181, 134]
The number of points in its cluster: 43

3. centroid is  [215, 161]
The number of points in its cluster: 90

4. centroid is  [257, 159]
The number of points in its cluster: 75

5. centroid is  [258, 113]
The number of points in its cluster: 38

***The plot was written to the 'plot.pdf' file.***

---------------------------------------------------

-The pdf file of this terminal example is in repo.
