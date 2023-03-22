public class TestClass
{
    public TestClass() {}

    public void recurse(int i)
    {
        recurse(i + 1);
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