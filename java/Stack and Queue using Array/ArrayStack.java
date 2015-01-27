/**
 * ArrayStack
 * Implementation of a stack using
 * an array as a backing structure
 *
 * @author Victor Lin
 * @version 2.0
 */
public class ArrayStack<T> implements StackADT<T> {

    // Do not add instance variables
    private T[] backing;
    private int size;

    /**
     * Construct an ArrayStack with
     * an initial capacity of INITIAL_CAPACITY.
     *
     * Use constructor chaining.
     */
    public ArrayStack() {
        this(INITIAL_CAPACITY);
    }

    /**
     * Construct an ArrayStack with the specified
     * initial capacity of initialCapacity
     * @param initialCapacity Initial capacity of the backing array.
     */
    public ArrayStack(int initialCapacity) {
        backing = (T[]) new Object[initialCapacity];
        size = 0;
    }

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
    public void push(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Data can't be null!");
        }
        if (size == backing.length) {
            resize();
        }
        //the index of the array for the next push
        //will always coincide with the size of the stack.
        backing[size] = data;
        size++;
    }

    /**
     * Helper function creates an array twice the current size,
     * copies all the values from the original backing array into it,
     * then sets it as the new backing array.
     * <p/>
     * Makes sure the new front and back values are correct.
     */
    private void resize() {
        T[] newArray = (T[]) new Object[backing.length * 2];
        copyData(newArray, backing);
        backing = newArray;
    }

    /**
     * Helper function copies all the values from the original backing array
     * into the new backing array.
     *
     * @param newArray the array to copy into
     * @param oldArray the array to copy from
     */
    private void copyData(T[] newArray, T[] oldArray) {
        for (int i = 0; i < oldArray.length; i++) {
            newArray[i] = oldArray[i];
        }
    }

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
    public T pop() {
        if (isEmpty()) {
            throw new java.util.NoSuchElementException(
                "Can't pop from an empty stack!");
        }
        T retValue = backing[size - 1];
        backing[size - 1] = null;
        size--;
        return retValue;
    }

    /**
     * Return the size of the stack.
     * Must be O(1)
     *
     * @return number of items in the stack
     */
    public int size() {
        return size;
    }

    /**
     * Return true if empty. False otherwise.
     * Must be O(1)
     *
     * @return boolean representing whether the list is empty
     */
    public boolean isEmpty() {
        return size == 0;
    }

    /**
     * Returns the backing array for your queue.
     * This is for grading purposes only. DO NOT EDIT THIS METHOD.
     *
     * @return the backing array
     */
    public Object[] getBackingArray() {
        return backing;
    }
}
