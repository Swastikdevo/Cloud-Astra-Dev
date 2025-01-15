```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [filter, setFilter] = useState('');

  useEffect(() => {
    // Fetch customers from API or local storage
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const handleAddCustomer = () => {
    setCustomers([...customers, { ...newCustomer, id: Date.now() }]);
    setNewCustomer({ name: '', email: '' });
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        name="name" 
        placeholder="Customer Name"
        value={newCustomer.name}
        onChange={handleInputChange}
      />
      <input 
        type="email" 
        name="email" 
        placeholder="Customer Email"
        value={newCustomer.email}
        onChange={handleInputChange}
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <input 
        type="text" 
        placeholder="Search Customers"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```