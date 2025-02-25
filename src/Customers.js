```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [filteredCustomers, setFilteredCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
    setFilteredCustomers(data);
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    const filtered = customers.filter(customer =>
      customer.name.toLowerCase().includes(e.target.value.toLowerCase())
    );
    setFilteredCustomers(filtered);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search customers..."
        value={searchTerm}
        onChange={handleSearch}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```