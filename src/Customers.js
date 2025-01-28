```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const addCustomer = async (e) => {
    e.preventDefault();
    const newCustomer = { name, email };
    await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    setName('');
    setEmail('');
    fetchCustomers();
  };

  const deleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    fetchCustomers();
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <form onSubmit={addCustomer}>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Customer Name" required />
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Customer Email" required />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```