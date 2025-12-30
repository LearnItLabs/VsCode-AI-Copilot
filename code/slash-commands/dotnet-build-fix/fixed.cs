using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ErrorZone.BuildErrors;

internal class Fixed
{



  internal async Task Show()
  {
    int result = await Multiply(3, 8);
    Console.WriteLine($"Result: {result}");
  }


  internal async Task<int> Multiply(int a, int b)
  {
    await Task.Delay(10);
    return a * b;
  }


}
