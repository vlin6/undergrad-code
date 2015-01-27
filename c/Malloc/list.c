#include <stdlib.h>
#include "./LIST.h"
#include "my_malloc.h"

static NODE* create_node(int data);

/** create_NODE
  *
  * Helper function that creates a NODE by allocating memory for it on the heap.
  * Be sure to set its pointers to NULL.
  *
  * @param data a void pointer to data the user wants to store in the LIST
  * @return a NODE
  */
static NODE* create_node(int data)
{
    NODE* a = (NODE*) my_malloc (sizeof(NODE));
    if (a == NULL)
    {
	printf("We did not successfully create a NODE because we've ran out of memory.");
	return NULL;
    }
    a->prev = NULL;
    a->next = NULL;
    a->data = data;
    return a;
}

/** create_LIST
  *
  * Creates a LIST by allocating memory for it on the heap.
  * Be sure to initialize size to zero and head/tail to NULL.
  *
  * @return an empty linked LIST
  */
LIST* create_list(void)
{
    LIST* l = (LIST*) malloc(sizeof(LIST));
    if (l == NULL)
    {
      printf("We've ran out of memory and did not successfully create a LIST.");
      return NULL;
    }
    l->head = NULL;
    l->tail = NULL;
    l->size = 0;
    return l;
}

/**
 * pushFront
 * Takes in ptr to a LIST and data to add
 * Should add new NODE containing the data to the head of the LIST, and increment size
 */
void pushFront(LIST* list, int data)
{
 NODE* cur = create_node(data);
    if (cur == NULL)
    {
      printf("We've ran out of memory and did not successfully push the NODE to the front.");
      return;
    }
    if (list->size == 0)
    {
        list->tail = cur;
    }
    else
    {
      NODE* oldhead = list->head;
      oldhead->prev = cur;
      cur->next = oldhead;
    }
    list->head = cur;
    list->size++;
}

/**
 * pushBack
 * Takes in ptr to a LIST and data to add
 * Should add new NODE containing the data to the tail of the LIST, and increment size
 */
void pushBack(LIST* list, int data)
{
    NODE* cur = create_node(data);
    if (cur == NULL)
    {
      printf("We've ran out of memory and did not successfully push the NODE to the back.");
      return;
    }
    if(list->size == 0)
    {
        list->head = cur;
    }
    else
    {
      NODE* oldtail = list->tail;
      oldtail->next = cur;
      cur->prev = oldtail;
    }
    list->tail = cur;
    list->size++;
}

/**
 * popFront
 * Takes in ptr to a LIST
 * Remove and free NODE at the front of the LIST, and decrement size
 * Return the value of that NODE
 * Return 0 if the size of the LIST is 0
 */
int popFront(LIST* list)
{
    if (list->size == 0)
    {
      return 0;
    }
    NODE* cur_node = list->head;
    if (list->size == 1)
    {
      list->head = NULL;
      list->tail = NULL;
    }
    else
    {
      NODE* newhead = cur_node->next;
      newhead->prev = NULL;
      list->head = newhead;
    }
    list->size--;
      //do I need to free cur_NODE's prev and next?
    int data = cur_node->data;
    my_free(cur_node);
    return data;
}

/**
 * popBack
 * Takes in ptr to a LIST
 * Remove and free NODE at the back of the LIST, and decrement size
 * Return the value of that NODE
 * Return 0 if the size of the LIST is 0
 */
int popBack(LIST* list)
{
    NODE* cur_node = list->tail;
    if (list->size == 0)
    {
      return 0;
    }
    else if (list->size == 1)
    {
      list->head = NULL;
      list->tail = NULL;
    }
    else
    {
      NODE* newtail = cur_node->prev;
      newtail->next = NULL;
      list->tail = newtail;
    }
    list->size--;
      //do I need to free cur_NODE's prev and next?
    int data = cur_node->data;
    my_free(cur_node);
    return data;
}
