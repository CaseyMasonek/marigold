defr factorial(n) {
    guard (n == 0) 1;

    n * (self (n - 1));
}

putint (factorial 5);