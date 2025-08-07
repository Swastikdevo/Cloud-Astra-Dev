```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '', phone: '' });

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    setNewCustomer({ name: '', email: '', phone: '' });
    fetchCustomers();
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" value={newCustomer.name} onChange={handleInputChange} placeholder="Name" required />
        <input type="email" name="email" value={newCustomer.email} onChange={handleInputChange} placeholder="Email" required />
        <input type="text" name="phone" value={newCustomer.phone} onChange={handleInputChange} placeholder="Phone" required />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>{customer.name} - {customer.email} - {customer.phone}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```