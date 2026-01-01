using System.ComponentModel.DataAnnotations;

namespace RazorSimple.Models {
	public class Customer {
		public int Id { get; set; }

		[Required]
		[StringLength(50)]
		public string FirstName { get; set; } = string.Empty;

		[Required]
		[StringLength(50)]
		public string LastName { get; set; } = string.Empty;

		[Required]
		[EmailAddress]
		[StringLength(100)]
		public string Email { get; set; } = string.Empty;

		[Phone]
		[StringLength(20)]
		public string PhoneNumber { get; set; } = string.Empty;

		public DateTime DateOfBirth { get; set; }

		[StringLength(100)]
		public string City { get; set; } = string.Empty;

		[StringLength(50)]
		public string Country { get; set; } = string.Empty;

		public ExperienceLevel BikingExperience { get; set; }

		/// <summary>
		/// Indicates whether the customer has signed the required insurance waiver
		/// </summary>
		public bool HasSignedWaiver { get; set; } = false;

		public DateTime RegisteredAt { get; set; } = DateTime.UtcNow;

		// Computed properties
		public string FullName => $"{FirstName} {LastName}";

		public int Age => DateTime.Now.Year - DateOfBirth.Year -
				(DateTime.Now.DayOfYear < DateOfBirth.DayOfYear ? 1 : 0);
	}

	public enum ExperienceLevel {
		Beginner = 1,
		Recreational = 2,
		Intermediate = 3,
		Advanced = 4,
		Professional = 5
	}
}