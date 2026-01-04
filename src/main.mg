def say(n) {
    if ((n % 15) == 0) {
        put "fizzbuzz";
    } elif ((n % 3) == 0) {
        put "fizz";
    } elif ((n % 5) == 0) {
        put "buzz";
    } else {
        putint n;
    }
}

def fizzbuzz(n) {
    (RANGE n)
    | REVERSE
    | MAP SUCC
    | MAP say;
}

fizzbuzz 100;