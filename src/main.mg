def say(n) {
    if (n % 15 == 0) {
        put "fizzbuzz";
    } elif (n % 3 == 0) {
        put "fizz";
    } elif (n % 5 == 0) {
        put "buzz";
    } else {
        putint n;
    }
}

def fizzbuzz(n) {
    (RANGE n)
    | MAP SUCC
    | MAPL say;
}

fizzbuzz 100;

def isAdult(age) {
    if (age < 12) "kid"
    elif (age < 18) "teen"
    elif (age < 65) "adult"
    else "senior"
}

put (isAdult 16);