all: q6 q7

q6:

	gcc -Wall -o q6 q6.c
	./q6
q7:

	gcc -Wall -o q7 q7.c
	./q7

clean:
	rm *o q6 q7