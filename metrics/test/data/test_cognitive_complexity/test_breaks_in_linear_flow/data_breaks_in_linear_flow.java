public class TestClass {
    public TestClass() {

    }
    public void method1() {
        for (Integer i = 0; i < 10; i++) break;
        while (true) {
            break;
        }
         if (false)
        {
            if ("" == "a")
            {
                System.out.println("a");
            }
            else if ("" == "b")
            {
                System.out.println("b");
            }
            else 
            {
                System.out.println("");
            }
        }
        else if (true)
        {
            System.out.println("not right");
        }
        else 
        {
            System.out.println("something is wrong");
        }
        try
        {
            System.out.println("fail");
            throw new IllegalArgumentException("Failed");
        }
        catch (IllegalArgumentException ex)
        {
            System.out.println("failed");
        }
    }
}