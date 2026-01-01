using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorSimple.Data;
using RazorSimple.Models;

namespace RazorSimple.Pages.Tours
{
    public class DetailsModel : PageModel
    {
        private readonly TourRepository _tourRepository;
        private readonly TestimonialRepository _testimonialRepository;

        public DetailsModel(TourRepository tourRepository, TestimonialRepository testimonialRepository)
        {
            _tourRepository = tourRepository;
            _testimonialRepository = testimonialRepository;
        }

        public Tour? Tour { get; set; }
        public List<Testimonial> Testimonials { get; set; } = new List<Testimonial>();
        public double AverageRating { get; set; }

        public IActionResult OnGet(int id)
        {
            Tour = _tourRepository.GetTourById(id);
            
            if (Tour == null)
            {
                return NotFound();
            }

            Testimonials = _testimonialRepository.GetTestimonialsByTourId(id)
                .Where(t => t.IsApproved)
                .OrderByDescending(t => t.ReviewDate)
                .ToList();

            AverageRating = _testimonialRepository.GetAverageRatingForTour(id);

            return Page();
        }

        public string GetStarRating(int rating)
        {
            return new string('?', rating);
        }
    }
}