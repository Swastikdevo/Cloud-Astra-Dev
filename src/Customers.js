```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      // Replace with your API endpoint
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const addCustomer = () => {
    const newCustomer = { name, email };
    setCustomers([...customers, newCustomer]);
    setName('');
    setEmail('');
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.includes(filter) || customer.email.includes(filter)
  );

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
      <button onClick={addCustomer}>Add Customer</button>
      <input 
        type="text" 
        placeholder="Search" 
        value={filter} 
        onChange={(e) => setFilter(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```