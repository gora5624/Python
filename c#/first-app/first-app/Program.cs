using System;
using System.Runtime;

namespace first_app
{
    class Program
    {
        static void Main(string[] args)
        {
            string operation = "start";
            int widthList = 0;
            int heightList = 0;
            int widthFilm = 0;
            int heightFilm = 0;
            while (true)
                {
                switch (operation)
                {
                    case "start":
                        Console.WriteLine("Введите размеры листа для резки в миллиметрах.");
                        operation = "sizeList";

                        break;
                    case "sizeList":
                        Console.Write("Введите ширину: ");
                        widthList += Convert.ToInt32(Console.ReadLine());
                        Console.Write("Введите длинну: ");
                        heightList += Convert.ToInt32(Console.ReadLine());
                        Console.WriteLine($"Размер листа для резки {widthList} на {heightList}");
                        Console.WriteLine("Продолжить? Введите: да/нет");
                        string cont = Convert.ToString(Console.ReadLine());
                        bool flag = true;
                        while (flag)
                        {
                            switch (cont)
                            {
                                case "да":
                                    operation = "sizeFilm";
                                    flag = false;
                                    break;
                                case "нет":
                                    operation = "start";
                                    flag = false;
                                    break;
                                default:
                                    Console.WriteLine("Введите да или нет");
                                    cont = Convert.ToString(Console.ReadLine());
                                    flag = true;
                                    break;
                            }
                        }
                        break;
                    case "sizeFilm":
                        Console.Write("Введите ширину пленки:");
                        widthFilm += Convert.ToInt32(Console.ReadLine());
                        Console.Write("Введите длинну пленки:");
                        heightFilm += Convert.ToInt32(Console.ReadLine());
                        Console.WriteLine($"Размер пленки для резки {widthFilm} на {heightFilm}");
                        Console.WriteLine("Продолжить? Введите: да/нет");
                        string cont_2 = Convert.ToString(Console.ReadLine());
                        bool flag_2 = true;
                        
                        while (flag_2)
                        {
                            switch (cont_2)
                            {
                                case "да":
                                    operation = "calc";
                                    flag_2 = false;
                                    break;
                                case "нет":
                                    operation = "sizeFilm";
                                    flag_2 = false;
                                    break;
                                default:
                                    Console.WriteLine("Введите да или нет");
                                    cont_2 = Convert.ToString(Console.ReadLine());
                                    flag_2 = true;
                                    break;
                            }
                        }
                        break;
                    case "calc":
                        int numFilmWidth = widthList % widthFilm;
                        Console.WriteLine(numFilmWidth);
                        break;

                }
            }
            
        }
    }
}

