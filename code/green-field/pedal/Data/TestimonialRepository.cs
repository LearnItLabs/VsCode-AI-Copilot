using RazorSimple.Models;

namespace RazorSimple.Data
{
    public class TestimonialRepository
    {
        private static List<Testimonial> _testimonials = new List<Testimonial>
        {
      new Testimonial
      {
				Id = 1,
				TourId = 1,
				CustomerName = "John Smith",
				CustomerCity = "San Francisco",
				CustomerCountry = "USA",
				Review = "Amazing mountain trail experience! The views were absolutely breathtaking and our guide was knowledgeable and friendly. The challenging terrain was exactly what I was looking for. Highly recommend this tour to anyone seeking adventure.",
				Rating = 5,
				ReviewDate = DateTime.Now.AddDays(-15),
				IsApproved = true,
				IsFeatured = true
      },
      new Testimonial
      {
			Id = 2,
      TourId = 2,
      CustomerName = "Emily Johnson",
      CustomerCity = "Seattle",
      CustomerCountry = "USA",
      Review = "Perfect coastal ride for beginners! The pace was comfortable and the ocean views were stunning. Great way to spend a weekend. The bike rental was in excellent condition and the route was well-planned.",
      Rating = 4,
      ReviewDate = DateTime.Now.AddDays(-8),
      IsApproved = true,
			IsFeatured = false
      },
      new Testimonial
      {
        Id = 3,
        TourId = 1,
        CustomerName = "Michael Brown",
        CustomerCity = "Austin",
        CustomerCountry = "USA",
        Review = "Challenging and rewarding! As an experienced cyclist, I appreciated the difficulty level and the stunning mountain scenery. The tour was well-organized and safety was clearly a priority.",
        Rating = 5,
        ReviewDate = DateTime.Now.AddDays(-22),
        IsApproved = true,
        IsFeatured = true
      },
      new Testimonial
      {
				Id = 4,
				TourId = 3,
				CustomerName = "Sarah Davis",
				CustomerCity = "Portland",
				CustomerCountry = "USA",
				Review = "The desert adventure was incredible! I never expected the desert to be so beautiful. The wildlife spotting was a bonus and our guide shared fascinating insights about the ecosystem. A truly unique experience.",
				Rating = 5,
				ReviewDate = DateTime.Now.AddDays(-5),
				IsApproved = true,
				IsFeatured = true
      },
      new Testimonial
      {
        Id = 5,
        TourId = 4,
        CustomerName = "David Wilson",
        CustomerCity = "Denver",
        CustomerCountry = "USA",
        Review = "Countryside tour exceeded expectations! The combination of cycling through beautiful farmlands and local food tastings was perfect. Great for couples or anyone who enjoys both cycling and local cuisine.",
        Rating = 4,
        ReviewDate = DateTime.Now.AddDays(-12),
        IsApproved = true,
        IsFeatured = false
      },
      new Testimonial
      {
        Id = 6,
        TourId = 5,
        CustomerName = "Lisa Garcia",
        CustomerCity = "Phoenix",
        CustomerCountry = "USA",
        Review = "Great urban exploration! Discovered parts of Portland I never knew existed. The tour was informative and fun, perfect for locals and visitors alike. Highly recommend for a different perspective of the city.",
        Rating = 4,
        ReviewDate = DateTime.Now.AddDays(-3),
        IsApproved = true,
        IsFeatured = false
      },
      new Testimonial
      {
        Id = 7,
        TourId = 2,
        CustomerName = "Robert Taylor",
        CustomerCity = "Los Angeles",
        CustomerCountry = "USA",
        Review = "Relaxing coastal ride with beautiful scenery. The route was well-planned and the group size was perfect. The guide was friendly and accommodating to different skill levels.",
        Rating = 4,
        ReviewDate = DateTime.Now.AddDays(-18),
        IsApproved = true,
        IsFeatured = false
      },
      new Testimonial
      {
        Id = 8,
        TourId = 3,
        CustomerName = "Jennifer Martinez",
        CustomerCity = "San Diego",
        CustomerCountry = "USA",
        Review = "The desert tour was challenging but absolutely worth it! The landscapes were otherworldly and the physical challenge was exactly what I needed. Our guide was excellent and very safety-conscious.",
        Rating = 5,
        ReviewDate = DateTime.Now.AddDays(-7),
        IsApproved = true,
        IsFeatured = true
      }
        };

        public List<Testimonial> GetAllTestimonials()
        {
            return _testimonials;
        }

        public Testimonial? GetTestimonialById(int id)
        {
            return _testimonials.FirstOrDefault(t => t.Id == id);
        }

        public List<Testimonial> GetTestimonialsByTourId(int tourId)
        {
            return _testimonials.Where(t => t.TourId == tourId).ToList();
        }

        public List<Testimonial> GetApprovedTestimonials()
        {
            return _testimonials.Where(t => t.IsApproved).ToList();
        }

        public List<Testimonial> GetFeaturedTestimonials()
        {
            return _testimonials.Where(t => t.IsFeatured && t.IsApproved).ToList();
        }

        public List<Testimonial> GetTestimonialsByRating(int rating)
        {
            return _testimonials.Where(t => t.Rating == rating).ToList();
        }

        public List<Testimonial> GetRecentTestimonials(int days = 30)
        {
            var cutoffDate = DateTime.Now.AddDays(-days);
            return _testimonials.Where(t => t.ReviewDate >= cutoffDate).ToList();
        }

        public double GetAverageRatingForTour(int tourId)
        {
            var tourTestimonials = _testimonials.Where(t => t.TourId == tourId && t.IsApproved).ToList();
            return tourTestimonials.Any() ? tourTestimonials.Average(t => t.Rating) : 0.0;
        }

        public Dictionary<int, int> GetRatingDistribution()
        {
            var approvedTestimonials = _testimonials.Where(t => t.IsApproved);
            return approvedTestimonials
                .GroupBy(t => t.Rating)
                .ToDictionary(g => g.Key, g => g.Count());
        }

        public void AddTestimonial(Testimonial testimonial)
        {
            testimonial.Id = _testimonials.Any() ? _testimonials.Max(t => t.Id) + 1 : 1;
            testimonial.ReviewDate = DateTime.UtcNow;
            testimonial.IsApproved = false; // New testimonials need approval
            _testimonials.Add(testimonial);
        }

        public void UpdateTestimonial(Testimonial testimonial)
        {
            var existingTestimonial = _testimonials.FirstOrDefault(t => t.Id == testimonial.Id);
            if (existingTestimonial != null)
            {
                var index = _testimonials.IndexOf(existingTestimonial);
                _testimonials[index] = testimonial;
            }
        }

        public void DeleteTestimonial(int id)
        {
            var testimonial = _testimonials.FirstOrDefault(t => t.Id == id);
            if (testimonial != null)
            {
                _testimonials.Remove(testimonial);
            }
        }

        public void ApproveTestimonial(int id)
        {
            var testimonial = _testimonials.FirstOrDefault(t => t.Id == id);
            if (testimonial != null)
            {
                testimonial.IsApproved = true;
            }
        }

        public void FeatureTestimonial(int id)
        {
            var testimonial = _testimonials.FirstOrDefault(t => t.Id == id);
            if (testimonial != null && testimonial.IsApproved)
            {
                testimonial.IsFeatured = true;
            }
        }
    }
}