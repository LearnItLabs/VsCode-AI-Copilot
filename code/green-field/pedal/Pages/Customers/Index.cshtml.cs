using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorSimple.Data;
using RazorSimple.Models;

namespace RazorSimple.Pages.Customers
{
    public class IndexModel : PageModel
    {
        private readonly CustomerRepository _customerRepository;

        public IndexModel(CustomerRepository customerRepository)
        {
            _customerRepository = customerRepository;
        }

        public List<Customer> Customers { get; set; } = new List<Customer>();
        public string SearchTerm { get; set; } = string.Empty;
        public string Filter { get; set; } = string.Empty;
        public int CustomersWithWaiver { get; set; }
        public int CustomersWithoutWaiver { get; set; }

        public void OnGet(string searchTerm = "", string filter = "")
        {
            SearchTerm = searchTerm ?? string.Empty;
            Filter = filter ?? string.Empty;

            // Get statistics
            var allCustomers = _customerRepository.GetAllCustomers();
            CustomersWithWaiver = allCustomers.Count(c => c.HasSignedWaiver);
            CustomersWithoutWaiver = allCustomers.Count(c => !c.HasSignedWaiver);

            // Apply filters
            Customers = filter switch
            {
                "waiver" => _customerRepository.GetCustomersWithWaiver(),
                "no-waiver" => _customerRepository.GetCustomersWithoutWaiver(),
                _ => allCustomers
            };

            // Apply search
            if (!string.IsNullOrWhiteSpace(SearchTerm))
            {
                Customers = _customerRepository.SearchCustomers(SearchTerm)
                    .Where(c => filter switch
                    {
                        "waiver" => c.HasSignedWaiver,
                        "no-waiver" => !c.HasSignedWaiver,
                        _ => true
                    }).ToList();
            }

            // Sort by registration date (newest first)
            Customers = Customers.OrderByDescending(c => c.RegisteredAt).ToList();
        }

        public async Task<IActionResult> OnPostMarkWaiverSignedAsync(int id)
        {
            var customer = _customerRepository.GetCustomerById(id);
            if (customer != null)
            {
                customer.HasSignedWaiver = true;
                _customerRepository.UpdateCustomer(customer);
            }

            return RedirectToPage();
        }
    }
}