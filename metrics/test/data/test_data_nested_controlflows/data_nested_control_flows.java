public class data_nested_control_flows {
    public Main() {}

    public void method1() {
        Boolean a, b, c = true;
        Boolean d, e, f = false;
        List lst1, lst2 = new ArrayList();
        if (a) {
            if (b) {
                if (c) {
                    for(Integer i = 0; i < 10; i++) {
                        System.out.println("Violation");
                    }
                }
            }
        } else if (b) {
            if (c) {

            } else {
                while (true) {
                    if (e) {
                        System.out.print("Violation");
                    }
                }
            }
        } else {
            if (d) {

            }
        }
        if (a) {

        } else {
            if (b) {
                if (c) {
                    for(Integer i = 0; i < 10; i++) {
                        System.out.println("Violation");
                    }
                }
            }
        }
        for(Integer i = 0; i < 10; i++) {
            if (b) {
                if (c) {
                    for(Integer i2 = 0; i2 < 10; i2++) {
                        System.out.println("Violation");
                    }
                }
            }
        }
        while (true) {
            if (c) {
                if (f) {
                    System.out.print("Not a violation");
                }
            } else {
                while (true) {
                    if (e) {
                        System.out.print("Violation");
                    }
                }
            }
        }
    }
}
