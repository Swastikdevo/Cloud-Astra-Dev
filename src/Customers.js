```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [filters, setFilters] = useState({ name: '', email: '' });

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filters.name.toLowerCase()) &&
    customer.email.toLowerCase().includes(filters.email.toLowerCase())
  );

  return (
    <div>
      <h1>Customer List</h1>
      <input 
        type="text" 
        placeholder="Filter by name" 
        value={filters.name} 
        onChange={e => setFilters({ ...filters, name: e.target.value })} 
      />
      <input 
        type="text" 
        placeholder="Filter by email" 
        value={filters.email} 
        onChange={e => setFilters({ ...filters, email: e.target.value })} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```