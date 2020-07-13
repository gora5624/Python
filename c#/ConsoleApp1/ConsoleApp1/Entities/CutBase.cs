using System;
using System.Collections.Generic;
using System.Diagnostics.Eventing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class SizeList
    {
        public int Width { get; set; }
        public int Height { get; set; }
        protected virtual string ConsolName { get; set; }

        public SizeList()
        {
            ConsolName = "листа для резки";
            Width = 750;
            Height = 1040;
        }
        public SizeList(int width, int height)
        {
            ConsolName = "листа для резки";
            Width = width;
            Height = height;
        }

        public void SetSize()
        {
            bool result;
            do
            {
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine($"Введите ширину {ConsolName} в миллиметрах: ");
                int Num;
                result = int.TryParse((Console.ReadLine()), out Num);
                if ((result == true) && (Num > 0))
                {
                    Width = Num;
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("Принято");
                    break;
                }
                else if ((result == true) && (Num <= 0))
                {
                    result = false;
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Введите число больше 0");
                    continue;
                }
                else
                {
                    result = false;
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Введите положительное число цифрами с клавиатуры.");
                    continue;
                }
            }
            while (result == false);
            do
            {
                result = false;
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine($"Введите длинну {ConsolName} в миллиметрах: ");
                int Num;
                result = int.TryParse((Console.ReadLine()), out Num);
                if ((result == true) && (Num > 0))
                {
                    Height = Num;
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("Принято");
                    break;
                }
                else if ((result == true) && (Num <= 0))
                {
                    result = false;
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Введите число больше 0");
                    continue;

                }
                else
                {
                    result = false;
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Введите положительное число цифрами с клавиатуры.");
                    continue;
                }
            }
            while (result == false);

        }
    }
}
