CC = gcc
#Using -Ofast instead of -O3 might result in faster code, but is supported only by newer GCC versions
CFLAGS = -lm -pthread -O3  -march=native -Wall -funroll-loops -Wno-unused-result

all: word2vec 

word2vec : word2vec.c
	$(CC) -shared -o word2vec.so $(CFLAGS) -fPIC word2vec.c 

clean:
	rm -rf word2vec.so 
