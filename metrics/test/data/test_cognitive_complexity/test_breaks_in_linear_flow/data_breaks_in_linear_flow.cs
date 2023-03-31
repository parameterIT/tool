public class TestClass
{
    public TestClass() 
    { 
        if (true) 
        {
            Console.WriteLine("hello");
        }
    }
    public void method1() 
    {
        for (int i = 0; i < 10; i++) break;
        while (true)
        {
            continue;
        }
        if (false)
        {
            if ("" == "a")
            {
                Console.WriteLine("a");
            }
            else if ("" == "b")
            {
                Console.WriteLine("b");
            }
            else 
            {
                Console.WriteLine("");
            }
        }
        else if (true)
        {
            Console.WriteLine("not right");
        }
        else 
        {
            Console.WriteLine("something is wrong");
        }
        try
        {
            Console.WriteLine("fail");
            throw new ArgumentException("failed", "");
        }
        catch (Exception ex)
        {
            Console.WriteLine("failed");
        }
    }

}