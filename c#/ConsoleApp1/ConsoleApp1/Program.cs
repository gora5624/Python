using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Remoting;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
            SizeList sizeList = new SizeList();
            SizeFilm sizeFilm = new SizeFilm();
            Calculator Result = new Calculator();
            sizeList.SetSize();
            Console.WriteLine($"Ширина листа {sizeList.Width}, длинна листа {sizeList.Height}.");
            sizeFilm.SetSize();
            Console.WriteLine($"Ширина листа {sizeFilm.Width}, длинна листа {sizeFilm.Height}.");
            string result = Result.GetResult(sizeFilm, sizeList);
            Console.WriteLine(result);
            Console.ReadKey();
        }
    }
}

