defr fib(n) {
    if (n < 2) n
    else (self n - 1) + (self n - 2)
}

putint (fib 20) + 2;
