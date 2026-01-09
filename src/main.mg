module DequeueItem {
    # ADT representing data passed from Queue.Dequeue #

    def Cons(q,item) {
        # Initialize the data as a pair #
        (q,item);
    }

    def GetQueue(dq) {
        # Get the new queue #
        FIRST dq;
    }

    def GetDequeuedItem(dq) {
        # Get the dequeued item #
        SECOND dq;
    }
}

module Queue {
    # FIFO data structure with O(1) dequeue #

    def Cons(capacity) {
        # Inititalize the queue as a list contatining:
        A empty list to hold the data,
        The index of the front of the list
        The size of the data
        And the capacity#

        data = RANGE capacity; 
        data |= MAP (@n.nil);

        [data, 0, 0, capacity];
    }

    def FrontIndex(q) {
        # Returns the index of the first item in the queue #
        INDEX q 1;
    }

    def Size(q) {
        # Gets the number of items in the queue #
        INDEX q 2;
    }

    def GetRearIndex(q) {
        # Get the index of the last item of the queue #
        frontIdx = q | INDEX 1;
        size = q | INDEX 2;
        capacity = q | INDEX 3;
        
        (frontIdx + size) % capacity;
    }

    def GetFront(q) {
        # Get the first item of the queue #
        data = q | INDEX 0;
        frontIdx = q | INDEX 1;
        
        # Return the first item of the queue #
        data | INDEX frontIdx;
    }

    def Enqueue(q,item) {
        # Add item to the queue #
        data = q | INDEX 0;
        front = q | INDEX 1;
        size = q | INDEX 2;
        capacity = q | INDEX 3;
        dequeuedItem = q | INDEX 4;

        # If queue is full, do nothing #
        if (size == capacity) q
        else {
            # Otherwise #

            rearIndex = GetRearIndex q; # Get the index to add the item #
            newData = data | UPDATE rearIndex item; # Add item to data #
            newQ = q | UPDATE 0 newData; # Set data in queue #
            newQ |= UPDATE 2 (size++); # Increase size of the queue #

            newQ;
        }
    }

    def Dequeue(q) {
        # Remove the first item of the queue #
        data = q | INDEX 0;
        front = q | INDEX 1;
        size = q | INDEX 2;
        capacity = q | INDEX 3;

        if (size == 0) (DequeueItem q nil)
        else {
            first = GetFront q;

            newFront = (front++) % capacity;
            newSize = size--;
            newQ = UPDATE q 1 newFront;
            newQ |= UPDATE 2 newSize;

            # Return data as a DequeueItem #
            DequeueItem newQ first;
        }
    }

    def Describe(q,printfn) {
        # Print out the queue using a given print function #
        data = q | INDEX 0;
        front = q | INDEX 1;
        size = q | INDEX 2;
        capacity = q | INDEX 3;

        indeces = RANGE size;
        orderedIndeces = MAP indeces (@i.(i + front) % capacity);

        orderedIndeces | MAP (@n.INDEX data n) | MAPL printfn | @x.q;
    }
}

module Maze {
    def Cons(data) {
        # Initialize a new maze object, with data about the maze #

        rows = LEN maze;
        cols = LEN (INDEX maze 0);

        [data,rows,cols];
    }

    def At(maze,x,y) {
        # Get the item in the maze at give coordinates #
        data = maze | INDEX 0;
        rows = maze | INDEX 1;
        cols = maze | INDEX 2;

        if ((x > cols) || (y > rows)) 0
        else {
            data
            | INDEX y
            | INDEX x;
        }
    }
}

unpack Queue;
unpack DequeueItem;

Queue 5
| Enqueue "hi"
| Describe put;

import Queue;