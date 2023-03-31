public class TestClass {
    public TestClass() {
        if (a) { //1
            if (b) { //2
                break; //3
            }
        }
        for (Integer i = 0; i < 10; i++) //4
        {
            continue; //5
        }
        break;
        while(true) { //6
            System.out.println("Cool");
        }
    }
    public void method1() {
        if (a) { //1
            if (b) { //2
                method1(); //3
            }
        }
        for (Integer i = 0; i < 10; i++) //4
        {
            method1(); //5
        }
        while(true) { //6
            System.out.println("Cool");
        }
            
    }
}