/**
 * CS 2110 - Spring 2014 - Homework #12
 * Edited by: Brandon Whitehead, Andrew Wilder
 * Victor Lin
 * list.c: Complete the functions!
 */

#include <stdlib.h>
#include <stdio.h>
#include "list.h"

/* The node struct.  Has a prev pointer, next pointer, and data. */
/* DO NOT DEFINE ANYTHING OTHER THAN WHAT'S GIVEN OR YOU WILL GET A ZERO*/
/* Design consideration only this file should know about nodes */
/* Only this file should be manipulating nodes */
/* DO NOT TOUCH THIS DECLARATION DO NOT PUT IT IN OTHER FILES */
typedef struct lnode
{
  struct lnode* prev; /* Pointer to previous node */
  struct lnode* next; /* Pointer to next node */
  void* data; /* User data */
} node;


/* Do not create any global variables here. Your linked list library should obviously work for multiple linked lists */
// This function is declared as static since you should only be calling this inside this file.
static node* create_node(void* data);

/** create_node
  *
  * Helper function that creates a node by allocating memory for it on the heap.
  * Be sure to set its pointers to NULL.
  *
  * @param data a void pointer to data the user wants to store in the list
  * @return a node
  */
static node* create_node(void* data)
{
    node* a = (node*) malloc (sizeof(node));
    if (a == NULL)
    {
	printf("We did not successfully create a node because we've ran out of memory.");      
	return NULL;
    }
    a->prev = NULL;
    a->next = NULL;
    a->data = data;
    return a;
}

/** create_list
  *
  * Creates a list by allocating memory for it on the heap.
  * Be sure to initialize size to zero and head/tail to NULL.
  *
  * @return an empty linked list
  */
list* create_list(void)
{
    list* l = (list*) malloc(sizeof(list));
    if (l == NULL)
    {
      printf("We've ran out of memory and did not successfully create a list.");
      return NULL;
    }
    l->head = NULL;
    l->tail = NULL;
    l->size = 0;
    return l;
}

/** push_front
  *
  * Adds the data to the front of the linked list
  *
  * @param llist a pointer to the list.
  * @param data pointer to data the user wants to store in the list.
  */
void push_front(list* llist, void* data)
{
    node* cur = create_node(data);
    if (cur == NULL)
    {
      printf("We've ran out of memory and did not successfully push the node to the front.");
      return;
    }
    if (llist->size == 0)
    {
        llist->tail = cur;
    }
    else
    {
      node* oldhead = llist->head;
      oldhead->prev = cur;
      cur->next = oldhead;
    }
    llist->head = cur;
    llist->size++;
}

/** push_back
  *
  * Adds the data to the back/end of the linked list
  *
  * @param llist a pointer to the list.
  * @param data pointer to data the user wants to store in the list.
  */
void push_back(list* llist, void* data)
{
    node* cur = create_node(data);
    if (cur == NULL)
    {
      printf("We've ran out of memory and did not successfully push the node to the back.");
      return;
    }
    if(llist->size == 0)
    {
        llist->head = cur;
    }
    else
    {
      node* oldtail = llist->tail;
      oldtail->next = cur;
      cur->prev = oldtail;
    }
    llist->tail = cur;
    llist->size++;
}

/** front
  *
  * Gets the data at the front of the linked list
  * If the list is empty return NULL.
  *
  * @param llist a pointer to the list
  * @return The data at the first node in the linked list or NULL.
  */
void* front(list* llist)
{
    /// @todo Implement changing the return value!
    /// @note you are returning the HEAD's DATA not the head node. Remember the user should never deal with the linked list nodes.
    return llist->head->data;
}

/** back
  *
  * Gets the data at the "end" of the linked list
  * If the list is empty return NULL.
  *
  * @param llist a pointer to the list
  * @return The data at the last node in the linked list or NULL.
  */
void* back(list* llist)
{
    /// @todo Implement changing the return value!
    return llist->tail->data;
}

/** remove_front
  *
  * Removes the node at the front of the linked list
  *
  * @warning Note the data the node is pointing to is also freed. If you have any pointers to this node's data it will be freed!
  *
  * @param llist a pointer to the list.
  * @param free_func pointer to a function that is responsible for freeing the node's data.
  * @return -1 if the remove failed (which is only there are no elements) 0 if the remove succeeded.
  */
int remove_front(list* llist, list_op free_func)
{
    /// @todo Implement
    /// @note remember to also free the node itself
    /// @note free_func is a function that is responsible for freeing the node's data only.
    if (llist->size == 0)
    {
      return -1;
    }
    node* cur_node = llist->head;
    if (llist->size == 1)
    {
      llist->head = NULL;
      llist->tail = NULL;
    }
    else
    {
      node* newhead = cur_node->next;
      newhead->prev = NULL;
      llist->head = newhead;
    }
    llist->size--;
      //do I need to free cur_node's prev and next?
    (*free_func)(cur_node->data);
    free(cur_node);
    return 0;

}

/** remove_back
  *
  * Removes the node at the back of the linked list
  *
  * @warning Note the data the node is pointing to is also freed. If you have any pointers to this node's data it will be freed!
  *
  * @param llist a pointer to the list.
  * @param free_func pointer to a function that is responsible for freeing the node's data.
  * @return -1 if the remove failed 0 if the remove succeeded.
  */
int remove_back(list* llist, list_op free_func)
{
    /// @todo Implement
    /// @note Remember to also free the node itself
    /// @note free_func is a function that is responsible for freeing the node's data only.
    node* cur_node = llist->tail;
    if (llist->size == 0)
    {
      return -1;
    }
    else if (llist->size == 1)
    {
      llist->head = NULL;
      llist->tail = NULL;
    }
    else
    {
      node* newtail = cur_node->prev;
      newtail->next = NULL;
      llist->tail = newtail;
    }
    llist->size--;
      //do I need to free cur_node's prev and next?
    (*free_func)(cur_node->data);
    free(cur_node);
    return 0;
}

/** copy_list
  *
  * Create a new list structure, new nodes, and new copies of the data by using
  * the copy function. Its implementation for any test structure must copy
  * EVERYTHING!
  *
  * @param llist A pointer to the linked list to make a copy of
  * @param copy_func A function pointer to a function that makes a copy of the
  *        data that's being used in this linked list, allocating space for
  *        every part of that data on the heap. This is some function you must
  *        write yourself for testing, tailored specifically to whatever context
  *        you're using the linked list for in your test.
  * @return The linked list created by copying the old one
  */
list* copy_list(list* llist, list_cpy copy_func)
{
  int i;
  list* newlist = create_list();

  printf("We ran copy_list method!");

  if (newlist == NULL)
  {
    printf("We've ran out of memory and did not successfully create a list.");
    return NULL;
  }
  node* cur_node = llist->tail;
  newlist->tail = cur_node;
  for (i = 0; i < llist->size; i++)
  {
 	 //typedef void* (*list_cpy)(const void*);
    void* newdata = (*copy_func)(cur_node->data);
    push_front(newlist, newdata);
    cur_node = cur_node->prev;
  }
  
  return newlist;

  //void push_front(list* llist, void* data)
}

/** size
  *
  * Gets the size of the linked list
  *
  * @param llist a pointer to the list
  * @return The size of the linked list
  */
int size(list* llist)
{
    ///@note simply return the size of the linked list. It's that easy!
    return llist->size;
}

/** remove_if
  *
  * Removes all nodes whose data when passed into the predicate function returns true
  *
  * @param llist a pointer to the list
  * @param pred_func a pointer to a function that when it returns true it will remove the element from the list and do nothing otherwise @see list_pred.
  * @param free_func a pointer to a function that is responsible for freeing the node's data
  * @return the number of nodes that were removed.
  */
int remove_if(list* llist, list_pred pred_func, list_op free_func)
{
    /// @todo Implement changing the return value!
    /// @note remember to also free all nodes you remove.
    /// @note be sure to call pred_func on the NODES DATA to check if the node needs to be removed.
    /// @note free_func is a function that is responsible for freeing the node's data only.

    int nodes_removed = 0;
    node* cur_node = llist->head;
    node* temp;

    while (cur_node != NULL && llist->size != 0)
    {
	node* next_node = cur_node->next;      
	if((*pred_func)(cur_node->data))
      	{
        //check if both head and tail
        if(cur_node->prev == NULL && cur_node->next == NULL)
        {
          llist->head = NULL;
          llist->tail = NULL;
        }
        //check if head
        else if(cur_node->prev == NULL)
        {
          temp = cur_node->next;
          temp->prev = NULL;
          llist->head = temp;
        }
        //check if tail
        else if(cur_node->next == NULL)
        {
          temp = cur_node->prev;
          temp->next = NULL;
          llist->tail = temp;
        }
        else
        //neither tail nor head
        {
          //handle left node
          temp = cur_node->prev;
          temp->next = cur_node->next;
          //handle right node
          temp = cur_node->next;
          temp->prev = cur_node->prev;
        }
	(*free_func)(cur_node->data);
        free(cur_node);
        nodes_removed++;
        llist->size--;
      }
      cur_node = next_node;
    }
    return nodes_removed;
}

/** is_empty
  *
  * Checks to see if the list is empty.
  *
  * @param llist a pointer to the list
  * @return 1 if the list is indeed empty 0 otherwise.
  */
int is_empty(list* llist)
{
    ///@note an empty list by the way we want you to implement it has a size of zero and head points to NULL.
    return (llist->size == 0 && llist->head == NULL);
}

/** empty_list
  *
  * Empties the list after this is called the list should be empty.
  *
  * @param llist a pointer to a linked list.
  * @param free_func function used to free the node's data.
  */
void empty_list(list* llist, list_op free_func)
{
    /// @todo Implement
    /// @note Free all of the nodes not the linked list itself.
    /// @note do not free llist.
    while (remove_back(llist, free_func) != -1);
    llist->head = NULL;
    llist->tail = NULL;
}

/** traverse
  *
  * Traverses the linked list calling a function on each node's data.
  *
  * @param llist a pointer to a linked list.
  * @param do_func a function that does something to each node's data.
  */
void traverse(list* llist, list_op do_func)
{
    /// @todo Implement
    // typedef void (*list_op)(void*);
      //is it better to use a while loop to check for a node whose next is NULL?
    int i;
    node* cur_node = llist->head;
    for (i = 0; i < llist->size; i++) {
      (*do_func)(cur_node->data);
      cur_node = cur_node->next;
    }

}
