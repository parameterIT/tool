public class data_nested_control_flows {
    public Main() {
        Boolean e,r,t,y = true;
        if (e) {
            if (r) {
                if (t) {
                    if (y) {
                        System.out.println("Violation");
                    }
                }
            }
        }
    }

    public void method1() {
        Boolean a, b, c = true;
        String str, str2 = "";
        switch (str) {
            case "Some String":
                try {
                    switch (str2) {
                        case "Some new string":
                            if (b) {
                                System.out.println("Violation");
                            }
                            break;
                    }
                } catch (RuntimeException ex) {
                    System.out.println("nope");
                }
                break;

            default:
                System.out.println("Not a violation");
        }
    }
}
