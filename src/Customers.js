```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    fetch('/api/customers')
      .then(res => res.json())
      .then(data => {
        setCustomers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer({ ...newCustomer, [name]: value });
  };

  const addCustomer = () => {
    fetch('/api/customers', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newCustomer),
    })
      .then(res => res.json())
      .then(data => {
        setCustomers([...customers, data]);
        setNewCustomer({ name: '', email: '' });
      });
  };

  return (
    <div>
      <h1>Customer Management</h1>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error.message}</p>}
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
      <input name="name" value={newCustomer.name} onChange={handleInputChange} placeholder="Name" />
      <input name="email" value={newCustomer.email} onChange={handleInputChange} placeholder="Email" />
      <button onClick={addCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```