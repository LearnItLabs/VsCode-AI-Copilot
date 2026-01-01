using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorSimple.Data;
using RazorSimple.Models;

namespace RazorSimple.Pages.Customers
{
    public class EditModel : PageModel
    {
        private readonly CustomerRepository _customerRepository;

        public EditModel(CustomerRepository customerRepository)
        {
            _customerRepository = customerRepository;
        }

        [BindProperty]
        public Customer Customer { get; set; } = new Customer();

        public IActionResult OnGet(int id)
        {
            Customer = _customerRepository.GetCustomerById(id);

            if (Customer == null)
            {
                return NotFound();
            }

            return Page();
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            // Check if email is being changed and if it already exists for another customer
            var existingCustomer = _customerRepository.GetCustomerByEmail(Customer.Email);
            if (existingCustomer != null && existingCustomer.Id != Customer.Id)
            {
                ModelState.AddModelError("Customer.Email", "A customer with this email already exists.");
                return Page();
            }

            _customerRepository.UpdateCustomer(Customer);

            TempData["Message"] = $"Customer '{Customer.FullName}' has been updated successfully.";
            return RedirectToPage("Details", new { id = Customer.Id });
        }

        public async Task<IActionResult> OnPostDeleteAsync(int id)
        {
            var customer = _customerRepository.GetCustomerById(id);
            if (customer == null)
            {
                return NotFound();
            }

            _customerRepository.DeleteCustomer(id);

            TempData["Message"] = $"Customer '{customer.FullName}' has been deleted successfully.";
            return RedirectToPage("Index");
        }
    }
}