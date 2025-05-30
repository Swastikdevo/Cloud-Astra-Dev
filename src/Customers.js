```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    fetch('/api/customers')
      .then(res => res.json())
      .then(data => setCustomers(data))
      .catch(err => console.error(err));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewCustomer(prev => ({ ...prev, [name]: value }));
  };

  const addCustomer = () => {
    setCustomers(prev => [...prev, newCustomer]);
    setNewCustomer({ name: '', email: '' });
  };

  const deleteCustomer = (email) => {
    setCustomers(prev => prev.filter(customer => customer.email !== email));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        name="name"
        placeholder="Name"
        value={newCustomer.name}
        onChange={handleInputChange}
      />
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={newCustomer.email}
        onChange={handleInputChange}
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.email}>
            {customer.name} - {customer.email}
            <button onClick={() => deleteCustomer(customer.email)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```