using ConsoleApp1.Entities;

namespace ConsoleApp1
{
    class SizeFilm : CutBase
    {
       public SizeFilm() 
        {
            Name = "Пленки";
            Width = 104;
            Height = 179;
        }

        public SizeFilm(int width, int height)
        {
            Name = "Пленки";
            Width = width;
            Height = height;
        }
    }
}
