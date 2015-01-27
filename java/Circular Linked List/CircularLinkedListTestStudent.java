import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

/**
 * These are some simple test cases to get you started with testing your code.
 * Passing these does NOT guarantee any sort of grade
 * Not every method has been tested
 */
public class CircularLinkedListTestStudent {
    private LinkedListInterface<String> list;

    @Before
    public void setup() {
        list = new CircularLinkedList<String>();
    }

    @Test(timeout = 200)
    public void testAdd1() {
        assertTrue(list.isEmpty());
        assertEquals(0, list.size());

        list.addToFront("1");
        assertEquals(1, list.size());

        list.addToFront("2");
        assertEquals(2, list.size());

        list.addToFront("3");
        assertEquals(3, list.size());

        LinkedListNode<String> node = list.getHead();
        assertEquals("3", node.getData());

        node = node.getNext();
        assertEquals("2", node.getData());

        node = node.getNext();
        assertEquals("1", node.getData());

        //Make sure list is circular
        node = node.getNext();
        assertEquals("3", node.getData());

        //Go backwards
        node = node.getPrevious();
        assertEquals("1", node.getData());

        node = node.getPrevious();
        assertEquals("2", node.getData());
    }

    @Test(timeout = 200)
    public void testAdd2() {
        assertTrue(list.isEmpty());
        assertEquals(0, list.size());

        list.addToBack("3");
        assertEquals(1, list.size());

        list.addToBack("2");
        assertEquals(2, list.size());

        list.addToBack("1");
        assertEquals(3, list.size());

        LinkedListNode<String> node = list.getHead();
        assertEquals("3", node.getData());

        node = node.getNext();
        assertEquals("2", node.getData());

        node = node.getNext();
        assertEquals("1", node.getData());

        //Make sure list is circular
        node = node.getNext();
        assertEquals("3", node.getData());

        //Go backwards
        node = node.getPrevious();
        assertEquals("1", node.getData());

        node = node.getPrevious();
        assertEquals("2", node.getData());
    }

    @Test(timeout = 200)
    public void testRemove1() {
        assertTrue(list.isEmpty());
        assertEquals(0, list.size());

        list.addToFront("1");
        assertEquals(1, list.size());

        list.addToFront("2");
        assertEquals(2, list.size());

        list.addToFront("3");
        assertEquals(3, list.size());

        assertEquals("3", list.removeFromFront());
        assertEquals(2, list.size());
        assertEquals("2", list.getHead().getData());
    }

    @Test(timeout = 200)
    public void testRemove2() {
        assertTrue(list.isEmpty());
        assertEquals(0, list.size());

        list.addToFront("1");
        assertEquals(1, list.size());

        list.addToFront("2");
        assertEquals(2, list.size());

        list.addToFront("3");
        assertEquals(3, list.size());

        assertEquals("1", list.removeFromBack());
        assertEquals(2, list.size());
        assertEquals("2", list.getHead().getPrevious().getData());
    }

    @Test(timeout = 200)
    public void testGet() {
        assertTrue(list.isEmpty());
        assertEquals(0, list.size());

        list.addToFront("1");
        assertEquals(1, list.size());

        list.addToFront("2");
        assertEquals(2, list.size());

        list.addToFront("3");
        assertEquals(3, list.size());

        assertEquals("3", list.get(0));
        assertEquals("2", list.get(1));
        assertEquals("1", list.get(2));
        assertEquals(3, list.size());

        for (Object i: list.toArray()) {
            System.out.println(i);
        }
    }
}
