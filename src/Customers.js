```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  
  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);
  
  const handleChange = (e) => {
    setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    if (response.ok) {
      const addedCustomer = await response.json();
      setCustomers([...customers, addedCustomer]);
      setNewCustomer({ name: '', email: '' });
    }
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={newCustomer.name}
          onChange={handleChange}
          placeholder="Customer Name"
          required
        />
        <input
          type="email"
          name="email"
          value={newCustomer.email}
          onChange={handleChange}
          placeholder="Customer Email"
          required
        />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```