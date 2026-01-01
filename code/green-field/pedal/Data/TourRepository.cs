using RazorSimple.Models;

namespace RazorSimple.Data {
	public class TourRepository {
		private static List<Tour> _tours = new List<Tour>
	{
			new Tour
			{
				Id = 1,
				Name = "Scenic Mountain Trail",
				Description = "Experience breathtaking mountain views on this challenging trail through the Rocky Mountains. Perfect for experienced riders looking for an adventure.",
				DurationDays = 3,
				DistanceKm = 125.5,
				Difficulty = DifficultyLevel.Advanced,
				Price = 450.00m,
				StartLocation = "Denver, Colorado",
				EndLocation = "Aspen, Colorado",
				StartDate = DateTime.Now.AddDays(30),
				EndDate = DateTime.Now.AddDays(33),
				MaxParticipants = 12,
				CurrentParticipants = 8,
				ImageUrl = "/images/mountain-trail.jpg",
				IsActive = true,
				CreatedAt = DateTime.Now.AddDays(-60)
			},
			new Tour
			{
				Id = 2,
				Name = "Coastal Breeze Ride",
				Description = "Enjoy a relaxing ride along the beautiful Pacific coastline. Suitable for all kill levels with stunning ocean views.",
				DurationDays = 2,
				DistanceKm = 85.2,
				Difficulty = DifficultyLevel.Beginner,
				Price = 275.00m,
				StartLocation = "Santa Barbara, California",
				EndLocation = "Monterey, California",
				StartDate = DateTime.Now.AddDays(15),
				EndDate = DateTime.Now.AddDays(17),
				MaxParticipants = 20,
				CurrentParticipants = 15,
				ImageUrl = "/images/coastal-ride.jpg",
				IsActive = true,
				CreatedAt = DateTime.Now.AddDays(-45)
			},
			new Tour
			{
				Id = 3,
				Name = "Desert Adventure",
				Description = "Explore the rugged beauty of the Sonoran Desert on this intermediate-level tour. Discover unique wildlife and stunning landscapes.",
				DurationDays = 4,
				DistanceKm = 180.0,
				Difficulty = DifficultyLevel.Intermediate,
				Price = 595.00m,
				StartLocation = "Phoenix, Arizona",
				EndLocation = "Tucson, Arizona",
				StartDate = DateTime.Now.AddDays(45),
				EndDate = DateTime.Now.AddDays(49),
				MaxParticipants = 15,
				CurrentParticipants = 6,
				ImageUrl = "/images/desert-adventure.jpg",
				IsActive = true,
				CreatedAt = DateTime.Now.AddDays(-30)
			},
			new Tour
			{
				Id = 4,
				Name = "Countryside Farm Tour",
				Description = "Cycle through picturesque farmlands and enjoy fresh local produce tastings at family farms. A perfect combination of cycling and culinary experiences with farm-to-table meals.",
				DurationDays = 2,
				DistanceKm = 65.8,
				Difficulty = DifficultyLevel.Beginner,
				Price = 385.00m,
				StartLocation = "Napa, California",
				EndLocation = "Sonoma, California",
				StartDate = DateTime.Now.AddDays(60),
				EndDate = DateTime.Now.AddDays(62),
				MaxParticipants = 18,
				CurrentParticipants = 12,
				ImageUrl = "/images/countryside-farms.jpg",
				IsActive = true,
				CreatedAt = DateTime.Now.AddDays(-20)
			},
			new Tour
			{
				Id = 5,
				Name = "Urban Explorer",
				Description = "Discover the city's hidden gems on this urban cycling adventure. Visit historic neighborhoods, parks, and local landmarks.",
				DurationDays = 1,
				DistanceKm = 35.0,
				Difficulty = DifficultyLevel.Beginner,
				Price = 125.00m,
				StartLocation = "Portland, Oregon",
				EndLocation = "Portland, Oregon",
				StartDate = DateTime.Now.AddDays(10),
				EndDate = DateTime.Now.AddDays(10),
				MaxParticipants = 25,
				CurrentParticipants = 20,
				ImageUrl = "/images/urban-explorer.jpg",
				IsActive = true,
				CreatedAt = DateTime.Now.AddDays(-10)
			}

	};
		
		public List<Tour> GetAllTours() {
			return _tours;
		}

		public Tour? GetTourById(int id) {
			return _tours.FirstOrDefault(t => t.Id == id);
		}

		public List<Tour> GetActiveTours() {
			return _tours.Where(t => t.IsActive).ToList();
		}

		public List<Tour> GetAvailableTours() {
			return _tours.Where(t => t.IsAvailable).ToList();
		}

		public List<Tour> GetToursByDifficulty(DifficultyLevel difficulty) {
			return _tours.Where(t => t.Difficulty == difficulty).ToList();
		}

		public List<Tour> SearchTours(string searchTerm) {
			if (string.IsNullOrWhiteSpace(searchTerm))
				return _tours;

			var term = searchTerm.ToLower();
			return _tours.Where(t =>
					t.Name.ToLower().Contains(term) ||
					t.Description.ToLower().Contains(term) ||
					t.StartLocation.ToLower().Contains(term) ||
					t.EndLocation.ToLower().Contains(term)
			).ToList();
		}

		public void AddTour(Tour tour) {
			tour.Id = _tours.Any() ? _tours.Max(t => t.Id) + 1 : 1;
			tour.CreatedAt = DateTime.UtcNow;
			_tours.Add(tour);
		}

		public void UpdateTour(Tour tour) {
			var existingTour = _tours.FirstOrDefault(t => t.Id == tour.Id);
			if (existingTour != null)
			{
				var index = _tours.IndexOf(existingTour);
				_tours[index] = tour;
			}
		}

		public void DeleteTour(int id) {
			var tour = _tours.FirstOrDefault(t => t.Id == id);
			if (tour != null)
			{
				_tours.Remove(tour);
			}
		}
	}
}
