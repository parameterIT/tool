public class TestClass
{
    public TestClass() {}

    public void method1()
    {
        var a, b, c = true;
        var str = "";
        switch (str) 
        {
            case "Some String":
                if (b) 
                {
                    if (c) Console.WriteLine("NO");
                    else 
                    {
                        if (a) Console.WriteLine("VIOLATION");
                    }
                }
                break;
            case "Some other String":
                Console.WriteLine("Not a violation");
                break;
            default: 
                if (a)
                {
                    Console.WriteLine("Not a violation");
                }
        }
            
    }
}
