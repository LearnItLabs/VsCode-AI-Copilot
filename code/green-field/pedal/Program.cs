using RazorSimple.Data;

namespace RazorSimple {
	public class Program {
		public static void Main(string[] args) {
			var builder = WebApplication.CreateBuilder(args);

			// Add services to the container.
			builder.Services.AddRazorPages();

			// Register repositories
			builder.Services.AddSingleton<TourRepository>();
			builder.Services.AddSingleton<CustomerRepository>();
			builder.Services.AddSingleton<TestimonialRepository>();

			var app = builder.Build();

			// Configure the HTTP request pipeline.
			if (!app.Environment.IsDevelopment())
			{
				app.UseExceptionHandler("/Error");
				// The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
				//app.UseHsts();
			}


			app.UseStaticFiles();

			app.UseRouting();

			app.UseAuthorization();

			app.MapRazorPages();

			app.Run();


		}
	}
}
