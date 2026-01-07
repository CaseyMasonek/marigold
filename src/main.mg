module PList {
    pnil = (false,false);

    def Cons(x,y) {
        (true,(x,(true,y)));
    }

    def Head(p) {
        FIRST (SECOND p);
    }

    def Tail(p) {
        SECOND (SECOND p);
    }
}

myplist = PList 1 (PList 2 (PList 3 (PList 4 PList.pnil)));

t = (PList.Tail myplist);

h = PList.Head t;

putint h;