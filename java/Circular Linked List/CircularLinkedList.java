/**
 * CircularLinkedList implementation
 *
 * @author Victor Lin
 * @version 3.0
 */
public class CircularLinkedList<T> implements LinkedListInterface<T> {

    // Do not add new instance variables.
    private LinkedListNode<T> head;
    private int size;

    /**
     * Adds the element to the index specified.
     * Adding to indices 0 and size should be O(1), all other adds are O(n)
     * <p/>
     * Throw {@code java.lang.IndexOutOfBoundsException} if index is negative or
     * index > size.
     * Throw {@code java.lang.IllegalArgumentException} if data is null
     *
     * @param index The index where you want the new element.
     * @param data  Any object of type T.
     */
    public void addAtIndex(int index, T data) {
        if (data == null) {
            throw new java.lang.IllegalArgumentException("The data is null.");
        }
        if (index < 0 || index > size) {
            throw new java.lang.IndexOutOfBoundsException("The index is"
                    + " negative or index > size.");
        }
        if (index == 0) {
            addToFront(data);
        } else if (index == size) {
            addToBack(data);
        } else {
            addToBody(index, data);
        }
    }

    /**
     * Helper method adds a new node with the given data
     * to the body of the linked list at the index.
     * Updates the references for neighboring nodes and adjusts size.
     * <p/>
     * Throw {@code java.lang.IllegalArgumentException} if data is null
     *
     * @param index The index where you want the new element.
     * @param data  The data that the new node should hold.
     */
    private void addToBody(int index, T data) {
        if (data == null) {
            throw new java.lang.IllegalArgumentException("The data is null.");
        }
        LinkedListNode<T> newNode = new LinkedListNode<T>(data);
        LinkedListNode<T> oldNode = getNode(index);
        LinkedListNode<T> prevNode = oldNode.getPrevious();

        prevNode.setNext(newNode);
        oldNode.setPrevious(newNode);
        newNode.setNext(oldNode);
        newNode.setPrevious(prevNode);
        size++;
    }

    /**
     * Helper method traverses through the linked list
     * and returns node at given index.
     * <p/>
     * This method must be O(1) for index 0 and index (size-1).
     *
     * @param index The index of the element
     * @return current The requested node.
     */
    private LinkedListNode<T> getNode(int index) {
        LinkedListNode<T> current = head;
        if (index == size - 1) {
            current = current.getPrevious();
        } else if (index != 0) {
            int counter = 0;
            while (counter++ < index) {
                current = current.getNext();
            }
        }
        return current;
    }

    /**
     * Returns the element at the given index.
     * This method must be O(1) for index 0 and index (size-1).
     * O(n) is expected for all other indices.
     * <p/>
     * Throw java.lang.IndexOutOfBoundsException if index < 0 or index >= size
     *
     * @param index The index of the element
     * @return The object stored at that index.
     */
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new java.lang.IndexOutOfBoundsException("The index is "
                    + "negative or index > size.");
        }
        LinkedListNode<T> node = getNode(index);
        return node.getData();
    }

    /**
     * Removes and returns the element at index.
     * This method should be O(1) for index 0 and (size-1), and O(n) in all
     * other cases.
     * <p/>
     * Throw {@code java.lang.IndexOutOfBoundsException} if index < 0 or
     * index >= size.
     *
     * @param index The index of the element
     * @return The object that was formerly at that index.
     */
    public T removeAtIndex(int index) {
        if (index < 0 || index >= size) {
            throw new java.lang.IndexOutOfBoundsException("Index < 0"
                    + " or index >= size");
        } else if (index == 0) {
            return removeFromFront();
        } else if (index == size - 1) {
            return removeFromBack();
        } else {
            return removeFromBody(index);
        }
    }

    /**
     * Helper method removes a node located at the given index of
     * the linked list and returns the data it contains.
     * Updates the references for neighboring nodes and adjusts size.
     *
     * @param index The index of the requested node
     * @return data The data that the removed node held.
     */
    private T removeFromBody(int index) {
        LinkedListNode<T> retNode = getNode(index);
        LinkedListNode<T> prevNode = retNode.getPrevious();
        LinkedListNode<T> nextNode = retNode.getNext();

        prevNode.setNext(nextNode);
        nextNode.setPrevious(prevNode);
        size--;

        return retNode.getData();
    }

    /**
     * Add a new node to the front of your linked list
     * that holds the given data. Make sure to update head.
     * <p/>
     * Must be O(1)
     * <p/>
     * Throw {@code java.lang.IllegalArgumentException} if data is null
     *
     * @param data The data that the new node should hold.
     */
    public void addToFront(T data) {
        addToBack(data);
        //recognizes that in a circularly linked list, the only difference
        //between these two methods is the head adjustment.
        head = head.getPrevious();
    }

    /**
     * Add a new node to the back of your linked list
     * that holds the given data. Make sure to update tail.
     * <p/>
     * Must be O(1)
     * <p/>
     * Throw {@code java.lang.IllegalArgumentException} if data is null
     *
     * @param data The data that the new node should hold.
     */
    public void addToBack(T data) {
        if (data == null) {
            throw new java.lang.IllegalArgumentException("The data is null.");
        }
        LinkedListNode<T> newNode = new LinkedListNode<T>(data);
        if (isEmpty()) {
            head = newNode;
            head.setNext(head);
            head.setPrevious(head);
        } else {
            LinkedListNode<T> tail = head.getPrevious();
            head.setPrevious(newNode);
            tail.setNext(newNode);
            newNode.setPrevious(tail);
            newNode.setNext(head);
        }
        size++;
    }

    /**
     * Remove the front node from the list and return the
     * data from it.
     * <p/>
     * Must be O(1)
     *
     * @return The data from the front node or null.
     */
    public T removeFromFront() {
        if (size == 0) {
            return null;
        }
        LinkedListNode<T> retNode = head;
        if (size == 1) {
            head = null;
        } else {
            head = retNode.getNext();
            LinkedListNode<T> prevNode = retNode.getPrevious();
            LinkedListNode<T> nextNode = retNode.getNext();
            prevNode.setNext(nextNode);
            nextNode.setPrevious(prevNode);
        }
        size--;
        return retNode.getData();
    }

    /**
     * Remove the back node from the list and return the
     * data from it.
     * <p/>
     * Must be O(1)
     *
     * @return The data from the last node or null.
     */
    public T removeFromBack() {
        if (size == 0) {
            return null;
        }
        LinkedListNode<T> retNode = head.getPrevious();
        if (size == 1) {
            head = null;
        } else {

            LinkedListNode<T> prevNode = retNode.getPrevious();
            LinkedListNode<T> nextNode = retNode.getNext();
            prevNode.setNext(nextNode);
            nextNode.setPrevious(prevNode);
        }
        size--;
        return retNode.getData();
    }

    /**
     * Return the linked list represented as an array of objects.
     *
     * @return A copy of the linked list data as an array.
     */
    public Object[] toArray() {
        Object[] retArray = new Object[size()];
        LinkedListNode<T> current = head;
        for (int i = 0; i < size(); i++) {
            retArray[i] = current.getData();
            current = current.getNext();
        }

        return retArray;
    }

    /**
     * Return a boolean value representing whether or not
     * the list is empty.
     * <p/>
     * Must be O(1)
     *
     * @return True if empty. False otherwise.
     */
    public boolean isEmpty() {
        return size == 0;
    }

    /**
     * Return the size of the list as an integer.
     * <p/>
     * Must be O(1)
     *
     * @return The size of the list.
     */
    public int size() {
        return size;
    }

    /**
     * Clear the list.
     * <p/>
     * Must be O(1)
     */
    public void clear() {
        head = null;
        size = 0;
    }

    /**
     * Reference to the head node of the linked list.
     * Normally, you would not do this, but we need it
     * for grading your work.
     *
     * @return Node representing the head of the linked list
     */
    public LinkedListNode<T> getHead() {
        return head;
    }

}
