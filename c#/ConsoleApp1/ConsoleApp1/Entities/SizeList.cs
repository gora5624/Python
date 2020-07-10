using ConsoleApp1.Entities;

namespace ConsoleApp1
{
    class SizeList: CutBase
    {
        public SizeList()
        {
            Name = "Листа";
            Width = 750;
            Height = 1040;
        }
        public SizeList(int width, int height)
        {
            Name = "Листа";
            Width = width;
            Height = height;
        }
    }
}
