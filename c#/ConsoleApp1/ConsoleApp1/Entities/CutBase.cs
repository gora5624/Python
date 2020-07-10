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
                if (result == true)
                {
                    Width = Num;
                    break;
                }
            }
            while (result == false);
            do
            {
                Console.WriteLine($"Введите длинну {Name} для резки в миллиметрах: ");
                int Num;
                result = int.TryParse((Console.ReadLine()), out Num);
                if (result == true)
                {
                    Height = Num;
                    break;
                }
            }
            while (result == false);
        }
    }
}
