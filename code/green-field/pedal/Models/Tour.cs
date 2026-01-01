using System.ComponentModel.DataAnnotations;

namespace RazorSimple.Models {
	public class Tour {
		public int Id { get; set; }

		[Required]
		[StringLength(100)]
		public string Name { get; set; } = string.Empty;

		[Required]
		[StringLength(500)]
		public string Description { get; set; } = string.Empty;

		[Range(1, 30)]
		public int DurationDays { get; set; }

		[Range(0.1, 1000)]
		public double DistanceKm { get; set; }

		public DifficultyLevel Difficulty { get; set; }

		[Range(0, double.MaxValue)]
		public decimal Price { get; set; }

		[StringLength(200)]
		public string StartLocation { get; set; } = string.Empty;

		[StringLength(200)]
		public string EndLocation { get; set; } = string.Empty;

		public DateTime StartDate { get; set; }

		public DateTime EndDate { get; set; }

		public int MaxParticipants { get; set; }

		public int CurrentParticipants { get; set; }

		[StringLength(500)]
		public string ImageUrl { get; set; } = string.Empty;

		public bool IsActive { get; set; } = true;

		public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

		// Computed properties
		public bool IsAvailable => IsActive && CurrentParticipants < MaxParticipants && StartDate > DateTime.Now;

		public int AvailableSpots => MaxParticipants - CurrentParticipants;
	}

	public enum DifficultyLevel {
		Beginner = 1,
		Intermediate = 2,
		Advanced = 3,
		Expert = 4
	}
}