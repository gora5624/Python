using ConsoleApp1.Entities;

namespace ConsoleApp1
{
    class Calculator
    {
        public string GetResult(CutBase film, CutBase list)
        {
            int widthDiv = list.Width / film.Width;
            int wListhFilmDiv = list.Width / film.Height;
            int hListwFilmDiv = list.Height / film.Width;
            int heightDiv = list.Height / film.Height;

            bool resultFlag = widthDiv * heightDiv > wListhFilmDiv * hListwFilmDiv;

            int count = (resultFlag) 
                ? widthDiv * heightDiv 
                : wListhFilmDiv * hListwFilmDiv;

            string orient = (resultFlag) ? "вдоль" : "поперёк";


            return (count > 0) 
                ? $"Получится {count} шт. Располагать {orient}."
                : "Пленка слишком маленькая, попробуйте лист поменьше или пленку побольше :) ";
        }
    }
}
