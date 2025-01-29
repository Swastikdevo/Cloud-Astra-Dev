```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const handleChange = (e) => {
    setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('/api/customers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newCustomer),
    })
      .then(response => response.json())
      .then(data => {
        setCustomers([...customers, data]);
        setNewCustomer({ name: '', email: '' });
      });
  };

  const handleDelete = (id) => {
    fetch(`/api/customers/${id}`, {
      method: 'DELETE',
    }).then(() => setCustomers(customers.filter(customer => customer.id !== id)));
  };

  return (
    <div>
      <h2>Customer List</h2>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => handleDelete(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
      <h2>Add New Customer</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={newCustomer.name}
          onChange={handleChange}
          placeholder="Name"
          required
        />
        <input
          type="email"
          name="email"
          value={newCustomer.email}
          onChange={handleChange}
          placeholder="Email"
          required
        />
        <button type="submit">Add Customer</button>
      </form>
    </div>
  );
};

export default CustomerManagement;
```