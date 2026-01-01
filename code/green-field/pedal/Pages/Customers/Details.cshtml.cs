using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorSimple.Data;
using RazorSimple.Models;

namespace RazorSimple.Pages.Customers
{
    public class DetailsModel : PageModel
    {
        private readonly CustomerRepository _customerRepository;

        public DetailsModel(CustomerRepository customerRepository)
        {
            _customerRepository = customerRepository;
        }

        public Customer? Customer { get; set; }

        public IActionResult OnGet(int id)
        {
            Customer = _customerRepository.GetCustomerById(id);

            if (Customer == null)
            {
                return NotFound();
            }

            return Page();
        }

        public async Task<IActionResult> OnPostMarkWaiverSignedAsync(int id)
        {
            var customer = _customerRepository.GetCustomerById(id);
            if (customer == null)
            {
                return NotFound();
            }

            customer.HasSignedWaiver = true;
            _customerRepository.UpdateCustomer(customer);

            return RedirectToPage(new { id });
        }
    }
}