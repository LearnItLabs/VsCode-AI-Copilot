using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ErrorZone.BuildErrors;

internal class Broken {
	// Error 1: Cannot implicitly convert Task<int> to int

 
	internal void Show() {
		int result = Multiply(3, 8);
		Console.WriteLine($"Result: {result}");
	}
	internal int Multiply(int a, int b) {
		return a * b;
	}

	//internal async Task<int> Multiply(int a, int b) {
	//	await Task.Delay(10);
	//	return a * b;
	//}


}
