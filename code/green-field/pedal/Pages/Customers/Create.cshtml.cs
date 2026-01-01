using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorSimple.Data;
using RazorSimple.Models;

namespace RazorSimple.Pages.Customers
{
    public class CreateModel : PageModel
    {
        private readonly CustomerRepository _customerRepository;

        public CreateModel(CustomerRepository customerRepository)
        {
            _customerRepository = customerRepository;
        }

        [BindProperty]
        public Customer Customer { get; set; } = new Customer();

        public IActionResult OnGet()
        {
            return Page();
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            // Check if email already exists
            var existingCustomer = _customerRepository.GetCustomerByEmail(Customer.Email);
            if (existingCustomer != null)
            {
                ModelState.AddModelError("Customer.Email", "A customer with this email already exists.");
                return Page();
            }

            _customerRepository.AddCustomer(Customer);

            TempData["Message"] = $"Customer '{Customer.FullName}' has been created successfully.";
            return RedirectToPage("Index");
        }
    }
}