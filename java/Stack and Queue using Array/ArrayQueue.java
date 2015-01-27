/**
 * ArrayQueue
 * Implementation of a queue using
 * an array as the backing structure
 *
 * @author Victor Lin
 * @version 3.0
 */
public class ArrayQueue<T> implements QueueADT<T> {

    // Do not add instance variables
    private T[] backing;
    private int size;
    private int front;
    private int back;

    /**
     * Construct an ArrayQueue with an
     * initial capacity of INITIAL_CAPACITY
     * <p/>
     * Use Constructor Chaining
     */
    public ArrayQueue() {
        this(INITIAL_CAPACITY);
    }

    /**
     * Construct an ArrayQueue with the specified
     * initial capacity of initialCapacity
     *
     * @param initialCapacity Initial capacity of the backing array.
     */
    public ArrayQueue(int initialCapacity) {
        backing = (T[]) new Object[initialCapacity];
        size = 0;
        front = 0;
        back = 0;
    }

    /**
     * Add a node with the given data
     * to the back of your queue.
     * <p/>
     * For array-backed implementations,
     * regrow the backing array if it is full.
     * <p/>
     * Must be O(1) (amortized for array-backed)
     *
     * @param data The data to add.
     * @throws IllegalArgumentException if data is null
     */
    public void enqueue(T data) {
        if (data == null) {
            throw new IllegalArgumentException("Data can't be null!");
        }
        if (size == backing.length) {
            resize();
            back++;
        } else if (size == 0) {
            //special case where size = 1,
            //the front and back indices are equivalent
            back = front;
        } else {
            //this is the general case where we increment,
            //but not past the array length
            back = (back + 1) % backing.length;
        }
        backing[back] = data;
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
        copyData(newArray, backing); //valuesCopied - 1 = index
        backing = newArray;
    }

    /**
    * Helper function prints everything in the queue from index 0.
    */
    private void printAll() {
        for (int i = 0; i < backing.length; i++) {
            System.out.print(backing[i] + " ");
        }
    }

    /**
     * Helper function copies all the values from the original backing array
     * into the new backing array. Adjusts front, back, and size.
     *
     * @param oldArray the array to copy from
     * @param newArray the array to copy into
     */
    private void copyData(T[] newArray, T[] oldArray) {
        int numCopied = 0;
        int numToCopy = size;
        while (numCopied < numToCopy) {
            //we're using numCopied as an index, thus < not <=
            newArray[numCopied] = oldArray[front];
            numCopied++;
            front = (front + 1) % oldArray.length;
        }
        back = numCopied - 1;
    }

    /**
     * Dequeue from the front of your queue.
     * <p/>
     * For array-backed implementations:
     * - you do not need to shrink the backing array.
     * - you must put null in the dequeued element's spot.
     * <p/>
     * Must be O(1)
     *
     * @return The data from the front of the queue.
     * @throws java.util.NoSuchElementException if the queue is empty
     */
    public T dequeue() {
        if (isEmpty()) {
            throw new java.util.NoSuchElementException("The queue is empty!");
        }
        T item = backing[front];
        backing[front] = null;
        front = (front + 1) % backing.length;
        size--;
        return item;
    }

    /**
     * Return the size of the queue.
     * Must be O(1)
     *
     * @return number of items in the queue
     */
    public int size() {
        return size;
    }

    /**
     * Return true if empty. False otherwise.
     * Must be O(1)
     *
     * @return boolean representing whether the queue is empty
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
