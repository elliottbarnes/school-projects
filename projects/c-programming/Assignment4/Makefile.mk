all: q4

q4:

	gcc -Wall -o q4 q4.c
	./q4

clean:
	rm *o q4