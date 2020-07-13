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
<<<<<<< HEAD:c#/ConsoleApp1/ConsoleApp1/SizeList.cs
            ConsolName = "листа для резки";
            Width = 750;
            Height = 1040;
=======
            Name = "CutBase";
>>>>>>> d1684c525cbb2170973f70663a0dd4cdd7f0805c:c#/ConsoleApp1/ConsoleApp1/Entities/CutBase.cs
        }

        public CutBase(int width, int height)
        {
<<<<<<< HEAD:c#/ConsoleApp1/ConsoleApp1/SizeList.cs
            ConsolName = "листа для резки";
=======
>>>>>>> d1684c525cbb2170973f70663a0dd4cdd7f0805c:c#/ConsoleApp1/ConsoleApp1/Entities/CutBase.cs
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
<<<<<<< HEAD:c#/ConsoleApp1/ConsoleApp1/SizeList.cs
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine($"Введите ширину {ConsolName} в миллиметрах: ");
=======
                Console.WriteLine($"Введите ширину {Name} для резки в миллиметрах: ");
>>>>>>> d1684c525cbb2170973f70663a0dd4cdd7f0805c:c#/ConsoleApp1/ConsoleApp1/Entities/CutBase.cs
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
<<<<<<< HEAD:c#/ConsoleApp1/ConsoleApp1/SizeList.cs
                result = false;
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine($"Введите длинну {ConsolName} в миллиметрах: ");
=======
                Console.WriteLine($"Введите длинну {Name} для резки в миллиметрах: ");
>>>>>>> d1684c525cbb2170973f70663a0dd4cdd7f0805c:c#/ConsoleApp1/ConsoleApp1/Entities/CutBase.cs
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
<<<<<<< HEAD:c#/ConsoleApp1/ConsoleApp1/SizeList.cs

=======
>>>>>>> d1684c525cbb2170973f70663a0dd4cdd7f0805c:c#/ConsoleApp1/ConsoleApp1/Entities/CutBase.cs
        }
    }
}
