all: q4

q4:

	gcc -g -Wall -o q4 q4.c 
	./q4
	

clean:
	rm -rf *o main-copy