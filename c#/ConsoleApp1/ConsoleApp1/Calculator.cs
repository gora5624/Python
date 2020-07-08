using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class Calculator
    {
        public string GetResult(int WidthList, int HeightList, int WidthFilm, int HeightFlim)
        {
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
            
        }
    }
}
