//  Copyright 2013 Google Inc. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
#include <errno.h>
#include <string.h>


void initialize();
void print_vector();

const long long max_size = 2000;         // max length of strings
const long long N = 40;                  // number of closest words that will be shown
const long long max_w = 50;              // max length of vocabulary entries

typedef struct {
  long long words; 
  long long size; 
  char *vocab;
  char **vocab2;
  float *vectors;

} word_vectors;

float *temp;


word_vectors vectors; 
int main(int argc, char **argv){
  initialize();
  return 0;
}
void initialize(char *fname){
  FILE *f;
  char file_name[max_size];
  float len;
  long long a, b;

  strcpy(file_name, fname);
  printf("%s\n", file_name);
  f = fopen(file_name, "rb");
  if (f == NULL) {
    printf("Input file not found\n");
    return;
  }

  // get pre-trained vector parameters 
  fscanf(f, "%lld ", &vectors.words);
  fscanf(f, "%lld", &vectors.size);
  vectors.vocab2 = (char **)malloc((long long)vectors.words*sizeof(char*));
  for(a = 0; a < vectors.words; ++a) vectors.vocab2[a] = (char *) malloc(sizeof(char)*max_w);
  vectors.vectors = (float *)malloc(vectors.words * vectors.size * sizeof(float));
  if (vectors.vectors == NULL) {
    printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)vectors.words * vectors.size * sizeof(float) / 1048576, vectors.words, vectors.size);
    return;
  }

  printf("loading the vectors\n");
  // load the words and the vectors
  for (b = 0; b < vectors.words; b++) {
    a = 0;
    while (1) {
      vectors.vocab2[b][a] = fgetc(f);
      if (feof(f) || (vectors.vocab2[b][a] == ' ')) break;
      if ((a < max_w) && (vectors.vocab2[b][a] != '\n')) a++;
    }
    // vectors.vocab[b * max_w + a] = 0;
    vectors.vocab2[b][a] = 0;
    for (a = 0; a < vectors.size; a++) fread(&vectors.vectors[a + b * vectors.size], sizeof(float), 1, f);
    len = 0;
    
    // normalize the vectors to unit vectors 
    for (a = 0; a < vectors.size; a++) len += vectors.vectors[a + b *vectors.size] * vectors.vectors[a + b * vectors.size];
    len = sqrt(len);
    for (a = 0; a < vectors.size; a++) vectors.vectors[a + b * vectors.size] /= len;

    if(b%100000 == 0) printf("done %lld words ...\n", b);
  }
  fclose(f);
  temp = (float *) malloc(sizeof(float)*vectors.size);
}

char **get_vocab(){
    return vectors.vocab2;
}

long long word_count(){
    return vectors.words;
}

long long vector_size(){ 
  return vectors.size; 
}

float *get_vector(long long index){
    long long a = 0;
    if(index > vectors.words || index < 0) return NULL;

    for (a = 0; a < vectors.size; a++){
      temp[a] = vectors.vectors[a + index * vectors.size];
    }
    return temp;
}


void check(){
    print_vector(1000);
}

void print_vector(int index){
    int a; 
    printf("[");
    for (a = 0; a < vectors.size; a++) {
      printf("%lf, ", vectors.vectors[a + index* vectors.size]);
    }
    printf("]\n");
}

/*
int main(int argc, char **argv) {

  FILE *f;
  FILE *f1;
  char st1[max_size];
  char *bestw[N];
  char file_name[max_size], st[100][max_size];
  float dist, len, bestd[N], vec[max_size];
  long long words, size, a, b, c, d, cn, bi[100];
  char ch;
  float *M;
  char *vocab;
  float *listOfVectors[10];
  int wordNumber;

   f1 = fopen("example.txt","rb");
  if (f1 == NULL) {
  printf("Word file not found\n");
  return -1;
  }

 if (argc < 2) {
    printf("Usage: ./distance <FILE>\nwhere FILE contains word projections in the BINARY FORMAT\n");
    return 0;
  }
  strcpy(file_name, argv[1]);
  f = fopen(file_name, "rb");
  if (f == NULL) {
    printf("Input file not found\n");
    return -1;
  }
  fscanf(f, "%lld", &words);
  fscanf(f, "%lld", &size);
  vocab = (char *)malloc((long long)words * max_w * sizeof(char));
  for (a = 0; a < N; a++) bestw[a] = (char *)malloc(max_size * sizeof(char));
  M = (float *)malloc((long long)words * (long long)size * sizeof(float));
  if (M == NULL) {
    printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)words * size * sizeof(float) / 1048576, words, size);
    return -1;
  }
  for (b = 0; b < words; b++) {
    a = 0;
    while (1) {
      vocab[b * max_w + a] = fgetc(f);
      if (feof(f) || (vocab[b * max_w + a] == ' ')) break;
      if ((a < max_w) && (vocab[b * max_w + a] != '\n')) a++;
    }
    vocab[b * max_w + a] = 0;
    for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f);
    len = 0;
    for (a = 0; a < size; a++) len += M[a + b * size] * M[a + b * size];
    len = sqrt(len);
    for (a = 0; a < size; a++) M[a + b * size] /= len;
  }
  fclose(f);

 while(fscanf(f1, "%s", st1)==1)
 {
     wordNumber = 0;
    cn = 0;
    b = 0;
    c = 0;
    while (1) {
      st[cn][b] = st1[b];
      b++;
      c++;
      st[cn][b] = 0;
      if (st1[c] == 0) break;
      if (st1[c] == ' ') {

        cn++;
        b = 0;
        c++;
      }
    }
    cn++;

    for (a = 0; a < cn; a++) {
      for (b = 0; b < words; b++) if (!strcmp(&vocab[b * max_w], st[a])) break;
      if (b == words) b = -1;
      bi[a] = b;
      printf("\nWord: %s  Position in vocabulary: %lld\n", st[a], bi[a]);
      if (b == -1) {
        printf("Out of dictionary word!\n");
        break;
      }
    }
   if (b == -1) continue;

   for (a = 0; a < size; a++) vec[a] = 0;
    for (b = 0; b < cn; b++) {
      if (bi[b] == -1) continue;
      for (a = 0; a < size; a++) vec[a] += M[a + bi[b] * size];

	  listOfVectors[wordNumber]=vec;
 
	  wordNumber++;
 
	  //output vector
      printf("[");
      for (a = 0; a < size; a++){
        printf("%lf ,", vec[a]);
      }
      printf("]\n");
 
    }



   }
  return 0;
} */
