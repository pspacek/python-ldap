/* David Leonard <david.leonard@csee.uq.edu.au>, 2000. Public domain. */
#ifndef __h_LinkedList
#define __h_LinkedList

/* $Id: linkedlist.h,v 1.1 2000/07/27 16:08:58 leonard Exp $ */

typedef struct {
	PyObject_HEAD
} LinkedListObject;

typedef void * (*firstfunc)(LinkedListObject *);
typedef void * (*nextfunc)(LinkedListObject *, void *);
typedef PyObject * (*itemfunc)(LinkedListObject *, void *);

typedef struct {
	PyTypeObject            llt_type;
	PySequenceMethods       llt_sequence;
	firstfunc		llt_firstfn;
	nextfunc		llt_nextfn;
	itemfunc		llt_itemfn;
} LinkedListType;

void LinkedList_inittype(LinkedListType *, char *, size_t,
	firstfunc, nextfunc, itemfunc);

PyObject *LinkedList_new(LinkedListType *);

#endif /* __h_LinkedList */
