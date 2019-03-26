
Beyza Kurt - 160709017

FINDING THE SECOND SMALLEST ELEMENT IN THE ARRAY by using MIPS Assembly
	
	! The array and its size have to be given in the code.


	The program compares a[i] and a[i+1] and gives values to the smallest and the second smallest elements.
	
	If a[i] is less than a[i+1],
	   the smallest element will be a[i] and the second smallest will be a[i+1].
	   If size of the array is 2, the program jump to 'found'.
	   Else the program jumps to 'loop'.
	If a[i] is greater than a[i+1],
	   the smallest element will be a[i+1] and the second smallest will be a[i].
	   If size of the array is 2, the program jump to 'found'.
	   Else the program jumps to 'loop'.
	If a[i] is equal to a[i+1],
	   the smallest element will be a[i] and the second smallest will stay equal 0.
	   If size of the array is 2, the program jump to 'noSec'.
	   Else the program jumps to 'loop'.

	
	-loop-
	The program compares a[k] and the smallest element.
	
	If a[k] is greater than the smallest elements:
		If the smallest and the second smallest element are equal,
		  the second smallest element will be equal to a[k].
		If a[k] is less than the second smallest element,
		  the second smallest element will be equal to a[k].
		If the second smallest is less than a[k],
		  elements won't change.
	If a[k] is greater than the smallest element and less than the second smallest element,
	  the second smallest element will be equal to a[k].
	If a[k] is less than the smallest element,
	  the second smallest element will be equal to the smallest element and
	  the smallest element will be equal to a[k].
	If a[k] is equal to the smallest element,
	  the smallest and the second smallest elements won't change.

	If the comparison is done, the program jumps 'x'.


	-x-
	The program checks the value of the second smallest.

	If the second smallest and the smallest elements are equal to 0,
	  the array must be "0,0,...".
	  The program jumps 'noSec'.
	If the second smallest element is equal to 0, there are two options;
	  all elements may be same and the second element never changed (It is 0 at the beginning)
	  or the second smallest element may be really 0.
	  The program jumps 'cont'.
	If the second smallest element is not equal to 0,
	  there is no confusion.
	  The program jumps 'found'.


	-cont-
	The program looks a[j].
	We know the array is not "0,0,...".

	If a[j] is equal to 0, "0" is really an element in the array.
	  So, the second smallest is really equal to 0.
	  The program jumps 'found'.
	If the control is done and there is no element that is equal to 0.
	  So, all elements are same.
	  The program jumps 'noSec'.


	-found-
	The program prints "The second smallest is: " and adds the value of the second smallest element.
	The program jumps 'Exit'.


	-noSec-
	The program prints "No second smallest".
	The program jumps 'Exit'.


	-Exit-
	The program finishes working.

