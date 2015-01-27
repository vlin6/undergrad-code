/**
 * Interface for a Stack ADT
 *
 * DO NOT MODIFY THIS FILE
 * @author CS 1332 TAs
 * @version 1.0
 */
public interface StackADT<T> {

    public static final int INITIAL_CAPACITY = 10;
    /**
     * Push a new node onto the stack with the given data.
     *
     * For array-backed implementations,
     * regrow the backing array if it is full.
     *
     * Must be O(1) (amortized for array-backed)
     *
     * @param data The data to push.
     * @throws IllegalArgumentException if data is null.
     */
    void push(T data);

    /**
     * Pop from the stack.
     *
     * For array-backed implementations:
     * - you do not need to shrink the backing array
     * - you must put null in the popped element's slot.
     *
     * Must be O(1)
     *
     * @return Data from the top of the stack
     * @throws java.util.NoSuchElementException if the stack is empty.
     */
    T pop();

    /**
     * Return the size of the stack.
     * Must be O(1)
     *
     * @return number of items in the stack
     */
    int size();

    /**
     * Return true if empty. False otherwise.
     * Must be O(1)
     *
     * @return boolean representing whether the list is empty
     */
    boolean isEmpty();
}
