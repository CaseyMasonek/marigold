initial_board = [[0,0,0],[0,0,0],[0,0,0]];
initial_state = ((PAIR initial_board) 1);

def display(state) {
    state 
    | FIRST 
    | REVERSE 
    | MAP putlist 
    | REVERSE
    | PAIR (SECOND state);
}

def get_index(n) {
    x = n | MOD 3;
    y = n // 3;

    [x,y];
}

def get_item(state,n) {
    pos = get_index n;

    x = pos | INDEX 0;
    y = pos | INDEX 1;

    state 
    | FIRST 
    | INDEX y 
    | INDEX x;
}

def update_board(state,coords) {
    x = HEAD coords;
    y = HEAD (TAIL coords);

    board = FIRST state;
    player = SECOND state;

    new_row = board | INDEX y | UPDATE x player;
    
    board | UPDATE y new_row | PAIR player;
}

def update_turn(state) {
    board = FIRST state;
    player = SECOND state;

    new_player = player | MOD 2 | ADD 1;

    (PAIR board) new_player;
}

def move(state) {
    pos = askint "where would you like to play? ";
    index = get_index pos;
    item = (get_item state) pos;

    if ((item | putint) == 0) {
        state
        | update_board index
        | update_turn;
    } else {
        state | update_turn;
    }
}

def check_row(state,row_indeces) {
    board = FIRST state;

    row = row_indeces | MAP (@r.state | get_item r);

    item_one = row | INDEX 0;
    item_two = row | INDEX 1;
    item_three = row | INDEX 2;

    condition = (item_one == item_two)
    | AND (item_one == item_two)
    | AND (item_one != 0);

    if (condition) item_one else 0
}

def check_board(state) {
    winning_rows = [[0,1,2]];
    
    rows = winning_rows | MAP @r.(state | check_row r);

    SUM rows;
}

defr main(state) {
    new_state = state
    | display
    | move;
    
    winner = check_board new_state;

    self new_state;
}

