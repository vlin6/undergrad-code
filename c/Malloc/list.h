#ifndef LIST_H
#define LIST_H

typedef struct node {
	int data;
	struct node *next;
	struct node *prev;
} NODE;

typedef struct list {
	NODE *head;
	NODE *tail;
	int size;
} LIST;

void pushFront(LIST* list, int data);
void pushBack(LIST* list, int data);
int popFront(LIST* list);
int popBack(LIST* list);
LIST* create_list(void);

#endif
