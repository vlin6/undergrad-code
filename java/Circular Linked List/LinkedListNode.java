/**
 * The node class. Remember that this is a circular linked list.
 * <p/>
 * DO NOT MODIFY THIS FILE.
 *
 * @author CS 1332 TAs
 */
public class LinkedListNode<T> {
    private T data;
    private LinkedListNode<T> next;
    private LinkedListNode<T> previous;

    /**
     * Create a new linked list node with the given data object and no next
     * or previous node.
     *
     * @param data data to store in this node
     */
    public LinkedListNode(T data) {
        this(data, null, null);
    }

    /**
     * Create a new linked list node with the given data object, previous node,
     * and next node.
     *
     * @param data     data to store in the node
     * @param previous previous node
     * @param next     next node
     */
    public LinkedListNode(T data, LinkedListNode<T> previous,
                          LinkedListNode<T> next) {
        this.data = data;
        this.next = next;
        this.previous = previous;
    }

    /**
     * Get the next node.
     *
     * @return next node
     */
    public LinkedListNode<T> getNext() {
        return next;
    }

    /**
     * Set the next node.
     *
     * @param node new next node
     */
    public void setNext(LinkedListNode<T> node) {
        next = node;
    }

    /**
     * Get the previous node.
     *
     * @return previous node
     */
    public LinkedListNode<T> getPrevious() {
        return previous;
    }

    /**
     * Set the previous node.
     *
     * @param node new previous node
     */
    public void setPrevious(LinkedListNode<T> node) {
        previous = node;
    }

    /**
     * Get the data stored in the node.
     *
     * @return data in this node
     */
    public T getData() {
        return data;
    }
}
