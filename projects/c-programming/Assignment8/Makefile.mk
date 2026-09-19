all: q7

q7:

	gcc -Wall -o q7 q7.c
	./q7

clean:
	rm *o q7
