```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

  useEffect(() => {
    // Simulating fetching data from an API
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

  const addCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const addedCustomer = await response.json();
    setCustomers([...customers, addedCustomer]);
    setNewCustomer({ name: '', email: '' });
  };

  const deleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        name="name" 
        placeholder="Customer Name" 
        value={newCustomer.name} 
        onChange={handleChange} 
      />
      <input 
        type="email"
        name="email"
        placeholder="Customer Email"
        value={newCustomer.email}
        onChange={handleChange}
      />
      <button onClick={addCustomer}>Add Customer</button>
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