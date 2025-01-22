```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [filter, setFilter] = useState('');

  useEffect(() => {
    // Fetch customers from local storage or an API
    const fetchedCustomers = JSON.parse(localStorage.getItem('customers')) || [];
    setCustomers(fetchedCustomers);
  }, []);

  const addCustomer = () => {
    const updatedCustomers = [...customers, newCustomer];
    setCustomers(updatedCustomers);
    localStorage.setItem('customers', JSON.stringify(updatedCustomers));
    setNewCustomer({ name: '', email: '' });
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        placeholder="Filter by name" 
        value={filter} 
        onChange={e => setFilter(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
      <h2>Add New Customer</h2>
      <input 
        type="text" 
        placeholder="Name" 
        value={newCustomer.name} 
        onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })} 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={newCustomer.email} 
        onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })} 
      />
      <button onClick={addCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```