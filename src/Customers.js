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
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const data = await response.json();
    setCustomers([...customers, data]);
    setNewCustomer({ name: '', email: '' });
  };

  const handleDelete = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h1>Customer Management</h1>
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
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => handleDelete(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```