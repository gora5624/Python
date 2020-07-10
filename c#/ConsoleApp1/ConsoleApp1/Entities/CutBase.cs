using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1.Entities
{
    public abstract class CutBase
    {
        public int Width { get; set; }
        public int Height { get; set; }
        public string Name { get; protected set; }

        public CutBase() 
        {
            Name = "CutBase";
        }

        public CutBase(int width, int height)
        {
            Width = width;
            Height = height;
            Name = "CutBase";
        }

        //пускай так пока, мб потом переопределишь
        public virtual void SetSize()
        {
            bool result;
            do
            {
                Console.WriteLine($"Введите ширину {Name} для резки в миллиметрах: ");
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
                Console.WriteLine($"Введите длинну {Name} для резки в миллиметрах: ");
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
