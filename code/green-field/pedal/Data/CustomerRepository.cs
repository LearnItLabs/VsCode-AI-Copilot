using RazorSimple.Models;

namespace RazorSimple.Data {

	public class CustomerRepository {

		private static List<Customer> _customers = new List<Customer>
		{
		new Customer {
			Id = 1,
			FirstName = "John",
			LastName = "Smith",
			Email = "john.smith@email.com",
			PhoneNumber = "(555) 123-4567",
			DateOfBirth = new DateTime(1985, 3, 15),
			City = "San Francisco",
			Country = "USA",
			BikingExperience = ExperienceLevel.Intermediate,
			HasSignedWaiver = true,
			RegisteredAt = DateTime.Now.AddDays(-90)
			},
			new Customer
			{
				Id = 2,
				FirstName = "Emily",
				LastName = "Johnson",
				Email = "emily.johnson@email.com",
				PhoneNumber = "(555) 234-5678",
				DateOfBirth = new DateTime(1992, 7, 22),
				City = "Seattle",
				Country = "USA",
				BikingExperience = ExperienceLevel.Advanced,
				HasSignedWaiver = true,
				RegisteredAt = DateTime.Now.AddDays(-75)
			},
			new Customer
			{
				Id = 3,
				FirstName = "Michael",
				LastName = "Brown",
				Email = "michael.brown@email.com",
				PhoneNumber = "(555) 345-6789",
				DateOfBirth = new DateTime(1978, 11, 8),
				City = "Austin",
				Country = "USA",
				BikingExperience = ExperienceLevel.Professional,
				HasSignedWaiver = true,
				RegisteredAt = DateTime.Now.AddDays(-120)
			},
			new Customer
			{
				Id = 4,
				FirstName = "Sarah",
				LastName = "Davis",
				Email = "sarah.davis@email.com",
				PhoneNumber = "(555) 456-7890",
				DateOfBirth = new DateTime(1995, 1, 30),
				City = "Portland",
				Country = "USA",
				BikingExperience = ExperienceLevel.Beginner,
				HasSignedWaiver = false,
				RegisteredAt = DateTime.Now.AddDays(-30)
			},
			new Customer
			{
				Id = 5,
				FirstName = "David",
				LastName = "Wilson",
				Email = "david.wilson@email.com",
				PhoneNumber = "(555) 567-8901",
				DateOfBirth = new DateTime(1988, 9, 12),
				City = "Denver",
				Country = "USA",
				BikingExperience = ExperienceLevel.Recreational,
				HasSignedWaiver = true,
				RegisteredAt = DateTime.Now.AddDays(-60)
			},
			new Customer
			{
				Id = 6,
				FirstName = "Lisa",
				LastName = "Garcia",
				Email = "lisa.garcia@email.com",
				PhoneNumber = "(555) 678-9012",
				DateOfBirth = new DateTime(1983, 5, 18),
				City = "Phoenix",
				Country = "USA",
				BikingExperience = ExperienceLevel.Intermediate,
				HasSignedWaiver = false,
				RegisteredAt = DateTime.Now.AddDays(-45)
			}
		};

		public List<Customer> GetAllCustomers() {
			return _customers;
		}

		public Customer? GetCustomerById(int id) {
			return _customers.FirstOrDefault(c => c.Id == id);
		}

		public Customer? GetCustomerByEmail(string email) {
			return _customers.FirstOrDefault(c => c.Email.ToLower() == email.ToLower());
		}

		public List<Customer> GetCustomersByExperience(ExperienceLevel experience) {
			return _customers.Where(c => c.BikingExperience == experience).ToList();
		}

		public List<Customer> SearchCustomers(string searchTerm) {
			if (string.IsNullOrWhiteSpace(searchTerm))
				return _customers;

			var term = searchTerm.ToLower();
			return _customers.Where(c =>
					c.FirstName.ToLower().Contains(term) ||
					c.LastName.ToLower().Contains(term) ||
					c.Email.ToLower().Contains(term) ||
					c.City.ToLower().Contains(term) ||
					c.Country.ToLower().Contains(term)
			).ToList();
		}

		public void AddCustomer(Customer customer) {
			customer.Id = _customers.Any() ? _customers.Max(c => c.Id) + 1 : 1;
			customer.RegisteredAt = DateTime.UtcNow;
			_customers.Add(customer);
		}

		public void UpdateCustomer(Customer customer) {
			var existingCustomer = _customers.FirstOrDefault(c => c.Id == customer.Id);
			if (existingCustomer != null)
			{
				var index = _customers.IndexOf(existingCustomer);
				_customers[index] = customer;
			}
		}

		public void DeleteCustomer(int id) {
			var customer = _customers.FirstOrDefault(c => c.Id == id);
			if (customer != null)
			{
				_customers.Remove(customer);
			}
		}

		public List<Customer> GetRecentCustomers(int days = 30) {
			var cutoffDate = DateTime.Now.AddDays(-days);
			return _customers.Where(c => c.RegisteredAt >= cutoffDate).ToList();
		}

		public List<Customer> GetCustomersWithWaiver() {
			return _customers.Where(c => c.HasSignedWaiver).ToList();
		}

		public List<Customer> GetCustomersWithoutWaiver() {
			return _customers.Where(c => !c.HasSignedWaiver).ToList();
		}
	}
}