/**
 * This interface describes the public methods needed for
 * Linked List, which should be circularly linked and should
 * have a head and tail pointer.   A single element should point back to itself.
 * <p/>
 * We've given you the expected Big-O for each method this time around.
 * <p/>
 * DO NOT ALTER THIS FILE!!
 *
 * @author CS 1332 TAs
 */
public interface LinkedListInterface<T> {

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
    public void addAtIndex(int index, T data);

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
    public T get(int index);

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
    public T removeAtIndex(int index);

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
    public void addToFront(T data);

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
    public void addToBack(T data);

    /**
     * Remove the front node from the list and return the
     * data from it.
     * <p/>
     * Must be O(1)
     *
     * @return The data from the front node or null.
     */
    public T removeFromFront();

    /**
     * Remove the back node from the list and return the
     * data from it.
     * <p/>
     * Must be O(1)
     *
     * @return The data from the last node or null.
     */
    public T removeFromBack();

    /**
     * Return the linked list represented as an array of objects.
     *
     * @return A copy of the linked list data as an array.
     */
    public Object[] toArray();

    /**
     * Return a boolean value representing whether or not
     * the list is empty.
     * <p/>
     * Must be O(1)
     *
     * @return True if empty. False otherwise.
     */
    public boolean isEmpty();

    /**
     * Return the size of the list as an integer.
     * <p/>
     * Must be O(1)
     *
     * @return The size of the list.
     */
    public int size();

    /**
     * Clear the list.
     * <p/>
     * Must be O(1)
     */
    public void clear();

    /**
     * Reference to the head node of the linked list.
     * Normally, you would not do this, but we need it
     * for grading your work.
     *
     * @return Node representing the head of the linked list
     */
    public LinkedListNode<T> getHead();
}
