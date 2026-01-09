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
