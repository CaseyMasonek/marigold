defr fact(n) {
    # calculate n! #

    guard (n == 0) 1; # base case #

    n * (self n--);
}

putint (fact 5);