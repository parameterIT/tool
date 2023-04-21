public class TestClass
{
    public TestClass() 
    {
        if (a) //1
        {
            if (b) //2
            {
                if (c) //3
                {
                    if (d) //4
                    {
                        Console.WriteLine("VIOLATION"); //5
                    }
                }
            }
        }
        if (k) //6
        {
            Console.WriteLine("NOT A VIOLATION");
        }
    }

    
    public void method1()
    {
        if (z) //1
        {
            Console.WriteLine("NOT A VIOLATION");
        }
        for (int i = 0; i < 10; i++) //2
        {
            var lst = List<int>();
            foreach (var val in lst) //3
            {
                if (a) //4
                {
                    Console.WriteLine("NOT A VIOLATION");
                }
                else 
                {
                    if (b) //5
                    {
                        Console.WriteLine("VIOLATION"); //6
                    }
                }
            }
        }
    }
    public void method2()
    {
       if (a) //1
       {
            Console.WriteLine("NOT A VIOLATION");
       }
       else 
       {
            if (b) //2
            {
                if (k) //3
                {
                    Console.WriteLine("NOT A VIOLATION");
                }
            }
            else 
            {
                if (c) //4
                {
                        Console.WriteLine("NOT A VIOLATION");
                }
                else 
                {
                    if (d) //5
                    {
                        Console.WriteLine("VIOLAITON"); //6
                    }
                    
                }
            }
       }
    }
    public void method3()
    {
        if (a) //1
        {
            try
            {
                Console.WriteLine("NOT A VIOLATION");
            }
            catch (Exception ex) //2
            {
                for (int i = 0; i < 10; i++) //3
                {
                    while (true) //4
                    {
                        Console.WriteLine("Violation"); //5
                    }
                }
            }
        }
        else
        {
            if (b) //6
            {
                Console.WriteLine("NOT A VIOLATION"); 
            }
        }
    }
    public void method4()
    {
       if (a) //1
       {
            Console.WriteLine("NOT A VIOLATION");
            if (b) //2
            {
                Console.WriteLine("NOT A VIOLATION");
            }
       }
       else 
       {
            try
            {
                for (int i = 0; i < 10; i++) //3
                {
                    if (b) //4
                    {
                        Console.Violation("VIOLATION"); //5
                    }
                }
            }
            catch (Exception ex) //6
            {
                Console.WriteLine("NOT A VIOLATION");
            }
       }
    }
    public void method5()
    {
       switch (a) //1
       {
            case (a == "Some string"):
                Console.WriteLine("NOT A VIOLATION");
                break;
            default:
                if (b) //2
                {
                    if(e) //3
                    {
                        Console.WriteLine("NOT A VIOLATION");
                    }
                }
                else
                {
                    for (int i = 0; i < 10; i++) //4
                    {
                        if (c) //5
                        {
                            Console.WriteLine("VIOLLATION"); //6
                        }
                    }
                }
       }
    }
}