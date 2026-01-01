using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorSimple.Data;
using RazorSimple.Models;

namespace RazorSimple.Pages.Tours
{
    public class IndexModel : PageModel
    {
        private readonly TourRepository _tourRepository;
        private readonly TestimonialRepository _testimonialRepository;

        public IndexModel(TourRepository tourRepository, TestimonialRepository testimonialRepository)
        {
            _tourRepository = tourRepository;
            _testimonialRepository = testimonialRepository;
        }

        public List<Tour> Tours { get; set; } = new List<Tour>();
        public string SearchTerm { get; set; } = string.Empty;
        public DifficultyLevel? FilterDifficulty { get; set; }

        public void OnGet(string searchTerm = "", string difficulty = "")
        {
            SearchTerm = searchTerm ?? string.Empty;
            
            if (Enum.TryParse<DifficultyLevel>(difficulty, out var difficultyLevel))
            {
                FilterDifficulty = difficultyLevel;
            }

            Tours = _tourRepository.GetActiveTours();

            if (!string.IsNullOrWhiteSpace(SearchTerm))
            {
                Tours = _tourRepository.SearchTours(SearchTerm);
            }

            if (FilterDifficulty.HasValue)
            {
                Tours = Tours.Where(t => t.Difficulty == FilterDifficulty.Value).ToList();
            }
        }

        public double GetAverageRating(int tourId)
        {
            return _testimonialRepository.GetAverageRatingForTour(tourId);
        }

        public int GetTestimonialCount(int tourId)
        {
            return _testimonialRepository.GetTestimonialsByTourId(tourId).Where(t => t.IsApproved).Count();
        }
    }
}