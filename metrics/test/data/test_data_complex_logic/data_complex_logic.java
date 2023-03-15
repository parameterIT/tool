public class data_complex_logic {
    public data_argument_count() {

    }

    public void method1(String arg1) {
        Boolean a = true;
        Boolean b = true;
        Boolean c = true;
        Boolean d = false;
        Boolean e = false;
        Boolean f = false;
        if (a || b || c) return;
        if (a || b || c && d) return;
        if (a || b || c && d && e) return;
        else if (a || b || c && d && e && f) return;
        else System.out.println(":(");

        while (a || b || c && d && e && f) {return;}

        var variable = a || b || c && d && e && f;
        var variable2 = a || b || c;   
    }
}
