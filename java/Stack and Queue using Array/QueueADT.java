/**
 * Interface for a Queue ADT
 *
 * DO NOT MODIFY THIS FILE
 * @author CS 1332 TAs
 * @version 1.0
 */
public interface QueueADT<T> {

    public static final int INITIAL_CAPACITY = 10;
    /**
     * Add a node with the given data
     * to the back of your queue.
     *
     * For array-backed implementations,
     * regrow the backing array if it is full.
     *
     * Must be O(1) (amortized for array-backed)
     *
     * @param data The data to add.
     * @throws IllegalArgumentException if data is null
     */
    void enqueue(T data);

    /**
     * Dequeue from the front of your queue.
     *
     * For array-backed implementations:
     * - you do not need to shrink the backing array.
     * - you must put null in the dequeued element's spot.
     *
     * Must be O(1)
     *
     * @return The data from the front of the queue.
     * @throws java.util.NoSuchElementException if the queue is empty
     */
    T dequeue();

    /**
     * Return the size of the queue.
     * Must be O(1)
     *
     * @return number of items in the queue
     */
    int size();

    /**
     * Return true if empty. False otherwise.
     * Must be O(1)
     *
     * @return boolean representing whether the queue is empty
     */
    boolean isEmpty();
}
