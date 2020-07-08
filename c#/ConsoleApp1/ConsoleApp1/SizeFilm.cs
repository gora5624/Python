using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class SizeFilm : SizeList
    {
       protected override string ConsolName { get; set; } = "пленки";
       public SizeFilm() 
        {
            ConsolName = "пленки";
            Width = 104;
            Height = 179;
        }
        public SizeFilm(int width, int height)

        {
            ConsolName = "пленки";
            Width = width;
            Height = height;
        }
    }
}
