public class TestClass
{
    public TestClass() { }

    public void recurse(int i)
    {
        recurse(i + 1);

        recurse(i);
        recurse(1);

        Console.WriteLine(recurse(i + 2) + recurse(i + 3));

        return (recurse(5));
    }

    private void print(string s)
    {
        Console.WriteLine(s);
    }

    public void HelloWorld()
    {
        print("Hello world");
    }
}