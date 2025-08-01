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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const addCustomer = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer)
    });
    const addedCustomer = await response.json();
    setCustomers([...customers, addedCustomer]);
    setNewCustomer({ name: '', email: '' });
  };

  const deleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(c => c.id !== id));
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <form onSubmit={addCustomer}>
        <input
          type="text"
          name="name"
          value={newCustomer.name}
          placeholder="Name"
          onChange={handleInputChange}
          required
        />
        <input
          type="email"
          name="email"
          value={newCustomer.email}
          placeholder="Email"
          onChange={handleInputChange}
          required
        />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map(customer => (
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