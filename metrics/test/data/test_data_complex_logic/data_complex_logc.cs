public class TestClass
{
    public TestClass() {}

    public void method1()
    {
        var a, b, c = true;
        var d, e, f = false;
        if (a || b || c) return;
        if (a || b || c && d) return;
        if (a || b || c && d && e) return;
        else if (a || b || c && d && e && f) return;
        else return;

        while (a || b || c && d && e && f) {return;}

        var variable = a || b || c && d && e && f;
        var variable = a || b || c;   
    }
}