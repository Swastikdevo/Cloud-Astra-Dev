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

  const handleAddCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const addedCustomer = await response.json();
    setCustomers([...customers, addedCustomer]);
    setNewCustomer({ name: '', email: '' });
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
      <input
        name="name"
        value={newCustomer.name}
        onChange={handleInputChange}
        placeholder="Customer Name"
      />
      <input
        name="email"
        type="email"
        value={newCustomer.email}
        onChange={handleInputChange}
        placeholder="Customer Email"
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```