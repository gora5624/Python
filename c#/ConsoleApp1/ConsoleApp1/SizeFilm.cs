using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class SizeFilm : SizeList
    {
       protected override string ConsolName { get; set; } = "Пленки";
       public SizeFilm() 
        {
            ConsolName = "Пленки";
            Width = 104;
            Height = 179;
        }
        public SizeFilm(int width, int height)

        {
            ConsolName = "Пленки";
            Width = width;
            Height = height;
        }
    }
}
