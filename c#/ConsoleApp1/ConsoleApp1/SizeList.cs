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
            ConsolName = "Листа";
            Width = 750;
            Height = 1040;
        }
        public SizeList(int width, int height)
        {
            ConsolName = "Листа";
            Width = width;
            Height = height;
        }

        public void SetSize()
        {
            bool result;
            do
            {   
                Console.WriteLine($"Введите ширину {ConsolName} для резки в миллиметрах: ");
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
                Console.WriteLine($"Введите длинну {ConsolName} для резки в миллиметрах: ");
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
