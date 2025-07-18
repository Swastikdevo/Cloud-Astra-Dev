```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('All');

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const handleSearch = (e) => {
    setSearch(e.target.value);
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(search.toLowerCase()) &&
    (filter === 'All' || customer.status === filter)
  );

  return (
    <div>
      <input type="text" placeholder="Search Customers" value={search} onChange={handleSearch} />
      <select onChange={(e) => setFilter(e.target.value)} value={filter}>
        <option value="All">All</option>
        <option value="Active">Active</option>
        <option value="Inactive">Inactive</option>
      </select>
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.status}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```