```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [filteredCustomers, setFilteredCustomers] = useState([]);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setFilteredCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleAddCustomer = () => {
    const newCustomer = { name, email };
    setCustomers([...customers, newCustomer]);
    setFilteredCustomers([...customers, newCustomer]);
    setName('');
    setEmail('');
  };

  const handleSearch = (e) => {
    const keyword = e.target.value.toLowerCase();
    const results = customers.filter(customer => 
      customer.name.toLowerCase().includes(keyword) || 
      customer.email.toLowerCase().includes(keyword)
    );
    setFilteredCustomers(results);
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        placeholder="Search..." 
        onChange={handleSearch} 
      />
      <input 
        type="text" 
        value={name} 
        placeholder="Customer Name" 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type="email" 
        value={email} 
        placeholder="Customer Email" 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
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