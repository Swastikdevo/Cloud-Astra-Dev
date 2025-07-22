```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '', phone: '' });

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
      body: JSON.stringify(newCustomer),
      headers: { 'Content-Type': 'application/json' },
    });
    const addedCustomer = await response.json();
    setCustomers([...customers, addedCustomer]);
    setNewCustomer({ name: '', email: '', phone: '' });
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <form onSubmit={handleSubmit}>
        <input name="name" value={newCustomer.name} onChange={handleChange} placeholder="Name" required />
        <input name="email" value={newCustomer.email} onChange={handleChange} placeholder="Email" required />
        <input name="phone" value={newCustomer.phone} onChange={handleChange} placeholder="Phone" required />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```