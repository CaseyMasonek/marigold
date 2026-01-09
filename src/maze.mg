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