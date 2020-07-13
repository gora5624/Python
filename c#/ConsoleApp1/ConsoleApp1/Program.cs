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
<<<<<<< HEAD
            bool flag = false;
            do
            {
                SizeList sizeList = new SizeList();
                SizeFilm sizeFilm = new SizeFilm();
                Calculator Result = new Calculator();
                sizeList.SetSize();
                Console.WriteLine($"Ширина листа {sizeList.Width}, длинна листа {sizeList.Height}.");
                sizeFilm.SetSize();
                Console.WriteLine($"Ширина листа {sizeFilm.Width}, длинна листа {sizeFilm.Height}.");
                string result = Result.GetResult(sizeList.Width, sizeList.Height, sizeFilm.Width, sizeFilm.Height);
                Console.WriteLine(result);
                Console.ForegroundColor = ConsoleColor.White;
                bool flag_2;
                do
                {
                    Console.WriteLine("Считать заного? Введите: 'да' или 'нет'");
                    string Input = Console.ReadLine();
                    if (Input == "да")
                    {
                        flag = true;
                        flag_2 = true;
                    }
                    else if (Input == "нет")
                    {
                        flag = false;
                        flag_2 = true;
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("Введите дословно 'да' или 'нет', либо просто закройте окно с программой.");
                        flag_2 = false;
                    }
                }
                while (flag_2 == false);
                
            }
            while (flag == true);
=======
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
>>>>>>> d1684c525cbb2170973f70663a0dd4cdd7f0805c
        }
    }
}

