using ConsoleApp1.Entities;

namespace ConsoleApp1
{
    class Calculator
    {
        public string GetResult(CutBase film, CutBase list)
        {
<<<<<<< HEAD
            int WlWf = WidthList / WidthFilm;
            int WlHf = WidthList / HeightFlim;
            int HlWf = HeightList / WidthFilm;
            int HlHf = HeightList / HeightFlim;
            
            int Count = (WlWf * HlHf > WlHf * HlWf ? WlWf * HlHf : WlHf * HlWf);
            string orient = (WlWf * HlHf > WlHf * HlWf ? "вдоль" : "поперёк");
            

            if (Count > 0)
            {
                return $"Получится {Count} шт. Располагать {orient}.";
            }
            else
            {
                return $"Получится {Count} шт. Вероятно вы ввели размер листа меньше чем размер пленки.";
            }
            
=======
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
>>>>>>> d1684c525cbb2170973f70663a0dd4cdd7f0805c
        }
    }
}
