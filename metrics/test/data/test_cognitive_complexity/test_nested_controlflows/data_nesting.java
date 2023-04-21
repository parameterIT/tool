public class data_nested_control_flows {
    public Main() {
        Boolean e,r,t,y = true;
        if (e) { //1
            if (r) { //2
                if (t) { //3
                    if (y) { //4
                        System.out.println("Violation"); //5
                    }
                }
            }
        }
        if (k) { //6
            System.out.println("NOT A VIOLATION");
        }
    }

    public void method1() {
        if (a) { //1
            if (z) { //2
                System.out.println("NOT A VIOLAITON");
            }
        } else {
            if (b) { //3
                System.out.println("NOT A VIOLAITON");
            } else {
                if (c) { //4
                System.out.println("NOT A VIOLAITON");
                } else {
                    if (d) { //5
                        System.out.println("VIOLATION"); //6
                    }
                }
            }
        }
    }
    public void method2() {
        for (Integer i = 0; i < 10; i++) { //1
            try {
                System.out.println("NOT A VIOLATION"); //2
            } catch (RuntimeException ex) { //3
                if (a) { //4
                    System.out.println("NOT A VIOLATION");
                } else {
                    if (b) { //5
                        System.out.println("VIOLATION"); //6
                    }
                }
            }
        } 
    }
    public void method3() {
        for (Integer i = 0; i < 10; i++) { //1
            try {
                if (a) { //2
                    System.out.println("NOT A VIOLATION");
                } else {
                    if (b) { //3
                        System.out.println("VIOLATION"); //4
                    }
                }
            } catch (RuntimeException ex) { //5
                System.out.println("NOT A VIOLATION"); //6
            }
        } 
    }
    public void method4() {
        while (true) { //1
            if (a) { //2
                for (Integer i = 0; i < 10; i++) { //3
                    if (b) { //4
                        System.out.println("VIOLATION"); //5
                    }
                }
            }
            else {
                if (c) { //6
                    System.out.println("NOT A VIOLATION");
                }
            }
        }
    }
    public void method5() {
        switch(expression) { //1
        case x:
            System.out.println("NOT A VIOLATION");
            break;
        
        default:
            if (a) { //2
                for (Integer i = 0; i < 10; i++) { //3
                    if (b) { //4
                        System.out.println("VIOLATION"); //5
                    }
                }
            }
        }
        if (c) { //6
            System.out.println("NOT A VIOLATION");
        }
    }
}
