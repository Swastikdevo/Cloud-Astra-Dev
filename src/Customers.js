```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(res => res.json())
      .then(data => setCustomers(data))
      .catch(err => console.error(err));
  }, []);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Search Customers"
        value={searchTerm}
        onChange={handleSearch}
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