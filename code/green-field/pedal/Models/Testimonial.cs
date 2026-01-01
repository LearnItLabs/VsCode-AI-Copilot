using System.ComponentModel.DataAnnotations;

namespace RazorSimple.Models {
	public class Testimonial {
		public int Id { get; set; }

		public int TourId { get; set; }

		[Required]
		[StringLength(100)]
		public string CustomerName { get; set; } = string.Empty;

		[StringLength(100)]
		public string CustomerCity { get; set; } = string.Empty;

		[StringLength(50)]
		public string CustomerCountry { get; set; } = string.Empty;

		[Required]
		[StringLength(1000)]
		public string Review { get; set; } = string.Empty;

		[Range(1, 5)]
		public int Rating { get; set; }

		public DateTime ReviewDate { get; set; } = DateTime.UtcNow;

		public bool IsApproved { get; set; } = false;

		public bool IsFeatured { get; set; } = false;

		// Computed property for display
		public string StarRating => new string('?', Rating) + new string('?', 5 - Rating);

		public string ShortReview => Review.Length > 150 ? Review.Substring(0, 147) + "..." : Review;
	}
}