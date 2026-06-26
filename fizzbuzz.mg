def fizzbuzz(n) {
    if (n % 15 == 0) put "fizzbuzz"
    elif (n % 5 == 0) put "buzz"
    elif (n % 3 == 0) put "fizz"
    else putint n
}

RANGE 30
| MAPL @n.fizzbuzz n++;
