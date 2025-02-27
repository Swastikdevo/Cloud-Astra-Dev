```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search customers"
        value={searchTerm}
        onChange={handleSearch}
      />
      <ul>
        {customers
          .filter(customer => customer.name.toLowerCase().includes(searchTerm.toLowerCase()))
          .map(customer => (
            <li key={customer.id}>{customer.name}</li>
          ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```