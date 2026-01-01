using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorSimple.Data;
using RazorSimple.Models;

namespace RazorSimple.Pages.Testimonials
{
    public class IndexModel : PageModel
    {
        private readonly TestimonialRepository _testimonialRepository;
        private readonly TourRepository _tourRepository;

        public IndexModel(TestimonialRepository testimonialRepository, TourRepository tourRepository)
        {
            _testimonialRepository = testimonialRepository;
            _tourRepository = tourRepository;
        }

        public List<Testimonial> Testimonials { get; set; } = new List<Testimonial>();
        public List<Testimonial> FeaturedTestimonials { get; set; } = new List<Testimonial>();
        public List<Tour> Tours { get; set; } = new List<Tour>();
        public int? FilterTourId { get; set; }
        public int? FilterRating { get; set; }
        public double OverallAverageRating { get; set; }
        public Dictionary<int, int> RatingDistribution { get; set; } = new Dictionary<int, int>();

        public void OnGet(int? tourId = null, int? rating = null)
        {
            FilterTourId = tourId;
            FilterRating = rating;

            Tours = _tourRepository.GetActiveTours();
            
            Testimonials = _testimonialRepository.GetApprovedTestimonials();
            
            if (FilterTourId.HasValue)
            {
                Testimonials = Testimonials.Where(t => t.TourId == FilterTourId.Value).ToList();
            }
            
            if (FilterRating.HasValue)
            {
                Testimonials = Testimonials.Where(t => t.Rating == FilterRating.Value).ToList();
            }

            Testimonials = Testimonials.OrderByDescending(t => t.ReviewDate).ToList();

            FeaturedTestimonials = _testimonialRepository.GetFeaturedTestimonials()
                .OrderByDescending(t => t.ReviewDate)
                .Take(3)
                .ToList();

            var allApproved = _testimonialRepository.GetApprovedTestimonials();
            OverallAverageRating = allApproved.Any() ? allApproved.Average(t => t.Rating) : 0.0;
            RatingDistribution = _testimonialRepository.GetRatingDistribution();
        }

        public string GetTourName(int tourId)
        {
            return Tours.FirstOrDefault(t => t.Id == tourId)?.Name ?? "Unknown Tour";
        }

        public string GetStarRating(int rating)
        {
            return new string('?', rating);
        }
    }
}