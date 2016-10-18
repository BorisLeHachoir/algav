#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

#define min(a, b) (((a) < (b)) ? (a) : (b))
#define max(a, b) (((a) > (b)) ? (a) : (b))

#define ALPHABET_SIZE 128
#define MAXIMUM_WORD_SIZE 16

typedef struct PatriciaTries
{
	char key[ALPHABET_SIZE][MAXIMUM_WORD_SIZE];
	struct PatriciaTries* children[ALPHABET_SIZE];

} PatriciaTries;

PatriciaTries* emptyPatriciaTrie()
{
	int i;
	struct PatriciaTries* pt = malloc(sizeof(PatriciaTries));
	for(i=0;i<ALPHABET_SIZE;++i)
	{
		pt->key[i][0] = '\0';
		pt->children[i] = NULL;
	}
	return pt;
}

void printkey(PatriciaTries* pt)
{
	int i;
	if(pt->key != NULL)
	{
		printf("[");
		for(i=0; i<ALPHABET_SIZE; ++i)
		{
			if(pt->key[i] != NULL)
				printf("%s | ", pt->key[i]);
		}
		printf("]");
		printf("\n");
		for(i=0; i<ALPHABET_SIZE; ++i)
		{
			if(pt->children[i] != NULL)
				printkey(pt->children[i]);
		}
	}
}

char* commonPreffix(char* m1, char* m2)
{
	char *cpm1 = m1;
	char *cpm2 = m2;
	char *res;
	int size, i;

	if(!cpm1 || !cpm2)
		return NULL;
	while(*cpm1 || *cpm2)
	{
		if(*cpm1 != *cpm2)
			break;
		cpm1++;
		cpm2++;
	}

	size = cpm1 - m1;
	printf("Size: %d\n", size);
	res = malloc(size + 1 *sizeof(char));
	memcpy(res,m1,size);
	res[size] = '\0';
	return res;
}

int main (int argc, char *argv[]) {

	PatriciaTries* pt;
	pt = emptyPatriciaTrie();

	return EXIT_SUCCESS;	
}