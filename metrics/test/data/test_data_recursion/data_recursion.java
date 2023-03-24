public class data_recursion {
    public Main() {
    }

    public void recurse(Integer i) {
        recurse(i + 1);
    }

    public void Print(String s) {
        System.out.println(s);
    }

    public void HelloWorld() {
        Print("Hello World");
    }
}
