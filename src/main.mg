defr fib(n) {
    if (n < 2) 1 else {
        (self n-1) + (self n-2);
    }
}

def firstn(n) {
    n | RANGE | MAP fib;
}


(askint "how many fibbonacci nums? " )
| firstn 
| putlist;