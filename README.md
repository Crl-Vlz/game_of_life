## To run the code you need to locate your console in the folder of the project and execute the following command:
- python ./Code/gol.py "input_name".in
### where you should change the "input_name" for the name of the input you wanna run

## The program creates an output.txt file where all the values of every generation is printed
### The code implements a function that focus the plot at the area where exist cells, so don't show a plot of a lot of pixels and only there are few cells. This function can also adapt to the growing and translation of the cells.

## IMPORTANT: To keep secure the area of calculation of patterns, we added a padding of 1 to each size, so the universe size shows 2 more than the provided size. For eample, if you enter 200, the output size will be 202
