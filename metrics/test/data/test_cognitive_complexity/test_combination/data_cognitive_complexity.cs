public class TestClass
{
    public TestClass() 
    { 
        if (true)
        {
            if (false)
            {
                break;
            }
        }
        while (true)
        {
            continue;
        }
        try 
        {
            Console.WriteLine();
        }
        catch (Exception e)
        {
            Console.WriteLine();
        }
    }
    public void method1() 
    {
        if (true) 
        {
            if (false)
            {
                method1();
            }
        }
        while (true)
        {
            try
            {
                Console.WriteLine("E");
            }
            catch (Exception e)
            {
                continue;
            }
        }
    }

}