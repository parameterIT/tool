public class data_recursion {
    public Main() {
    }

    public void recurse(Integer i) {
        if (recurse(i + 1)) {
            recurse(i);
        } else {
            recurse(i+3);
        }
        System.out.println(recurse(2) + recurse(3));
        return recurse(i + 5);
    }

    public void Print(String s) {
        System.out.println(s);
    }

    public void HelloWorld() {
        Print("Hello World");
    }
}
