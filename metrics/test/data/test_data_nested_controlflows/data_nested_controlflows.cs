public class TestClass
{
    public TestClass() 
    {
        var e,r,t,y = true;
        if (e) 
        {
        	if (r) 
            {
           		if (t) 
                {
                	if (y) Console.WriteLine("violation");
                }
            }
        }
    }

    public void method1()
    {
        var list1, list2, list3 = new List<int>();
        var a, b, c = true;
        var d, e, f = false;
        if (a)
        {
            if(b)
            {
                if(c)
                {
                    var chars = new List<char>();
                    foreach (var ch in chars)
                    {
                        Console.WriteLine("Violation");
                    }
                }
            }
        }
        else if (b) 
        {
            if (c)
            {

            }
            else
            {
                foreach (var item in list1)
                {
                    if (c) Console.WriteLine("Violation");
                }
            }
        }
        else
        {

        }
        var items = new List<int>();
        foreach(var item in items)
        {
            Console.WriteLine("Not a vioaltion");
        }
        while(true)
        {
            foreach (var item in list2)
            {
                if (d)
                {
                
                }
                else
                {
                    if (a)
                    {
                        Console.WriteLine("violation");
                    }
                }
            }
        }
    }
}
