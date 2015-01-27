#include "my_malloc.h"
#include <math.h>
#include <stdint.h>
//By Victor Lin

/* You *MUST* use this macro when calling my_sbrk to allocate the
 * appropriate size. Failure to do so may result in an incorrect
 * grading!
 */
#define SBRK_SIZE 2048

/* If you want to use debugging printouts, it is HIGHLY recommended
 * to use this macro or something similar. If you produce output from
 * your code then you will receive a 20 point deduction. You have been
 * warned.
 */

//#define DEBUG
#ifdef DEBUG
#define DEBUG_PRINT(x) printf (x)
#else
#define DEBUG_PRINT(x)
#endif


/* make sure this always points to the beginning of your current
 * heap space! if it does not, then the grader will not be able
 * to run correctly and you will receive 0 credit. remember that
 * only the _first_ call to my_malloc() returns the beginning of
 * the heap. sequential calls will return a pointer to the newly
 * added space!
 * Technically this should be declared static because we do not
 * want any program outside of this file to be able to access it
 * however, DO NOT CHANGE the way this variable is declared or
 * it will break the autograder.
 */
void* heap;

/* our freelist structure - this is where the current freelist of
 * blocks will be maintained. failure to maintain the list inside
 * of this structure will result in no credit, as the grader will
 * expect it to be maintained here.
 * Technically this should be declared static for the same reasons
 * as above, but DO NOT CHANGE the way this structure is declared
 * or it will break the autograder.
 */
metadata_t* freelist[8];
/**** SIZES FOR THE FREE LIST ****
 * freelist[0] -> 16
 * freelist[1] -> 32
 * freelist[2] -> 64
 * freelist[3] -> 128
 * freelist[4] -> 256
 * freelist[5] -> 512
 * freelist[6] -> 1024
 * freelist[7] -> 2048
 */

void* my_malloc(size_t size)
{
	//We don't instantiate the heap if the request is too large.
	size_t total_size = size + sizeof(metadata_t);
	if (total_size > SBRK_SIZE)
	{
		ERRNO = SINGLE_REQUEST_TOO_LARGE;
		DEBUG_PRINT("Error: single request was too large.\n");
		return NULL;
	}

	//If size is 0, then malloc() returns NULL
	if(size == 0)
	{
		return NULL;
	}

	//Instantiate the heap.
	if (heap == NULL)
	{
		heap = my_sbrk(SBRK_SIZE);
		freelist[7] = heap;
		freelist[7]->prev = NULL;
		freelist[7]->next = NULL;
		freelist[7]->in_use = 0;
		freelist[7]->size = 2048;
		DEBUG_PRINT("Heap instantiated.\n");
	}

	int total_size_int = (int) total_size;
	int index = getIndex(total_size_int);

	//user should be returned where the memory block begins.
	//from the metadata, that's just one pointer arithmetic.
	metadata_t* block = getBlock(index);
	block->in_use = 1;
   	void* result = block + 1;
   	ERRNO = NO_ERROR;

   	#ifdef DEBUG
	printf("\nAllocating space for a block.\n"); //if size is not instantiated, it'll be zero. aka, the buddy doesn't exist.
	printf("Let's look at the metadata's address and size.\n");
	printf("metadata address: %p\n", block);
	printf("metadata size: %d\n", block->size);
	#endif

	return result;
}

void* my_calloc(size_t num, size_t size)
{
  if (size == 0)
	{
		return NULL;
	}

  void* memory = my_malloc(num*size);

  if (memory == (void*) -1)
	{
		DEBUG_PRINT("Error: We have run out of memory.\n");
		ERRNO = OUT_OF_MEMORY;
		return NULL; //checks if we've run out of memory.
	}
  initialize(size, memory);
  ERRNO = NO_ERROR;

  return memory;
}

//setMem... use this to set all bytes of calloc to 0.
void initialize(size_t size, void* src)
{
	char* ptr = (char*)src;
	int i;
	for (i = 0; i < size; i++)
	{
		ptr[i] = 0;
	}
}

void my_free(void* ptr)
{
	DEBUG_PRINT("Calling my_free.\n");

	if (heap == NULL)
	{
		DEBUG_PRINT("Error: The heap hasn't been instantiated yet.\n");
		return;
	}

	//adjust the pointer to point at void*'s metadata_t
	metadata_t* a = (metadata_t*)((char*)ptr - sizeof(*a));
	//recall that a->size is the sum of both the metadata and requested space.
	int index = getIndex(a->size);
	a = merge(a, index);

	//current level, 'push'
	index = getIndex(a->size);
	metadata_t* oldhead = freelist[index]; //'push', rearranges the linked list for the new head
	a->prev = NULL;
	a->next = oldhead;
	if(oldhead) oldhead->prev = a;

	freelist[index] = a;
	ERRNO = NO_ERROR;
	return;
}

metadata_t* merge(metadata_t* ptr, int index)
{

	//make sure we're pointing to metadata_t
	metadata_t* a = ptr;
	a->in_use = 0; //this is the block we passed in and are trying to free
	metadata_t* b = getBuddy(ptr);


	if (index + 1 == 8 || b->size != a->size)
	{
		return a;
	}


	//resizes 'a' so now it is twice the size and points to next what b points to
	//if they're both free, then merge.
	//this means you'll have to rearrange two levels of linked lists.

	if (a->size == b->size && (!a->in_use && !b->in_use) )
	{
		DEBUG_PRINT("\nWe're merging.\n");

    	metadata_t* temp;

		//rearrange the buddies to make sure 'a' comes before 'b'


		#ifdef DEBUG
		printf("\nStats before we merge.\n"); //if size is not instantiated, it'll be zero. aka, the buddy doesn't exist.
		printf("Let's look at the a and b's address and size.\n");
		printf("a address: %p\n", a);
		printf("b size: %d\n", a->size);
		printf("a address: %p\n", b);
		printf("b size: %d\n", b->size);
		#endif

		//current level, 'pop' the buddy in the free list
		//we're trying to remove the buddy from the free list
		//'remove', rearranges the linked list for the new head

		if (b->prev == NULL)
		{
			freelist[index] = b->next;
			if(b->next) b->next->prev = NULL;
		} else {
			b->prev->next = b->next;
			if (b->next) {
			b->next->prev = b->prev;
			}
			b->prev = NULL;
			b->next = NULL;
		}


		if ((long)a - (long)b > 0) //if positive, a currently come after b. Switch.
		{
			temp = b;
			b = a;
			a = temp;
		}

		//next level, 'push'
		//'push', rearranges the linked list for the new head
		a->prev = NULL;
		a->size = (a->size)*2;
		a->next = NULL;

		a = merge(a, index + 1);
	}

	return a;
}

//Returns the buddy for a given block.
metadata_t* getBuddy(metadata_t* meta_ptr)
{
	//let's get the size, to calculate n, the bit we'd like to toggle to get the buddy.
	int meta_size = meta_ptr->size;
	int n = (int) log2(meta_size);
	long mask = 0x1 << n; //long because metadata is 8 bytes

	//subtract the heap from the meta_ptr.
	meta_ptr = (metadata_t*)((long)meta_ptr - (long)heap);

	//assures the n + 1th bit is the same
	metadata_t* buddy_ptr = meta_ptr;

	//toggles nth bit
	buddy_ptr = (metadata_t*)((long)buddy_ptr ^ mask);

	//restores heap to both
	meta_ptr = (metadata_t*)((long)meta_ptr + (long)heap);
	buddy_ptr = (metadata_t*)((long)buddy_ptr + (long)heap);

	#ifdef DEBUG
	printf("\nWe found a possible buddy.\n");
	printf("Let's look at the metadata and its buddy's address and size.\n");
	printf("metadata address: %p\n", meta_ptr);
	printf("metadata size: %d\n", meta_ptr->size);
	printf("buddy address: %p\n", buddy_ptr);
	printf("buddy size: %d\n", buddy_ptr->size);
	#endif

	return buddy_ptr;


}

void* my_memmove(void* dest, const void* src, size_t num_bytes)
{
  char* s = (char*) src;
  char* d = (char*) dest;
  char buffer[num_bytes];

  for (int i=0; i<num_bytes; i++) {
    buffer[i] = s[i];
  }

  for (int j=0; j<num_bytes; j++) {
  	d[j] = buffer[j];
  }
  ERRNO = NO_ERROR;
  return d;
}

//Given a size, returns the appropriate index corresponding to the freelist.
//e.g. input 31, output 1.
//31 fits in 32 = 2^5 = 2^m where m = 5. n = m - 4 = 1, freelist[1] holds 32 bits.
int getIndex(int sizeRequested)
{
	double expo;
	int result;
	expo = log2(sizeRequested); //gets you the exponent from base 2 as a double, so we can perform ceiling.
	expo = ceil(expo); //we use the smallest size that can contain our entire memory request.
	result = (int)expo - 4; //since we're start at 16, which is 2^n where n = 4.
	return result;
}

//Returns a block of free memory. Handles splitting if necessary.
metadata_t* getBlock(int index)
{
	//base case 1: free memory at the index
	metadata_t* memory;
	if (freelist[index]) //equivalent to freelist[index] != NULL;
	{
		memory = freelist[index];
		metadata_t* newhead = memory->next; //'pop', rearranges the linked list for the new head
		if (newhead) newhead->prev = NULL;
		freelist[index] = newhead;
		return memory;
	}

	//base case 2: no free memory at any of the indices
	if (index == 7) //to get here, freelist[index] must be NULL;
	{
		memory = my_sbrk(SBRK_SIZE);
		if (memory == (void*) -1)
		{
			DEBUG_PRINT("Error: We have run out of memory.\n");
			ERRNO = OUT_OF_MEMORY;
			return NULL; //checks if we've run out of memory.
		}
		memory->size = 2048;
		return memory;
	}

	//since I'm not at base case 1, it means I need to split to get free memory.
	//split. save one block on the freelist and return the other one.
    memory = getBlock(index + 1);
    if (memory == NULL) return NULL;
    int splitsize = memory->size/2;

    metadata_t* ret_mem;
    metadata_t* save_mem;

    //we'll return this block
    ret_mem = memory;
    ret_mem->size = splitsize;
    ret_mem->prev = NULL;
    ret_mem->next = NULL;
    ret_mem->in_use = 1;

    //we'll put this block on freelist
    save_mem = (metadata_t*)((char*)ret_mem + splitsize) ; //pointer arithmetic to arrive at the next metadata.
    save_mem->size = splitsize;
    save_mem->prev = NULL;
    save_mem->in_use = 0;

    metadata_t* oldhead = freelist[index]; //'push', rearranges the linked list for the new head
    save_mem->next = oldhead;
    freelist[index] = save_mem;

	return ret_mem;
}

//Prints the how many free memory are in each portion of the freelist.
void printfreelist()
{
	printf("\nRunning printfreelist.\n");
	int counter;
	metadata_t* node;
	int i;
	for (i = 0; i < 8; i++)
	{
		counter = 0;
		printf("Indexing into location: %d...", i);
		node = freelist[i];
		while (node != NULL)
		{
			counter++;
			//printf("Element %d in use? %d\n", counter, node->in_use);
			node = node->next;
		}
		printf("Found %d element(s).\n", counter);
	}
}
