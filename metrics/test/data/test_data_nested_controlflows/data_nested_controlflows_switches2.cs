switch (str) 
{
    case "Some String":
        if (b) 
        {
            switch (str2)
            {
                case "New string":
                    Console.WriteLine("Not a violation");
                    break;
                default:
                    if(a) Console.WriteLine("Violation");
                    break;
            }
        }
        break;
    case "Some other String":
        Console.WriteLine("Not a violation");
        break;
    default: 
        if (a)
        {
            Console.WriteLine("Not a violation");
        }
}