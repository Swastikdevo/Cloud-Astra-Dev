```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const handleAddCustomer = () => {
    const newCustomer = { name, email, active: true };
    setCustomers([...customers, newCustomer]);
    setName('');
    setEmail('');
  };

  const filteredCustomers = customers.filter(customer => {
    if (activeFilter === 'active') return customer.active;
    if (activeFilter === 'inactive') return !customer.active;
    return true;
  });

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        placeholder="Name" 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <select onChange={(e) => setActiveFilter(e.target.value)}>
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>{customer.name} - {customer.email} ({customer.active ? 'Active' : 'Inactive'})</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```