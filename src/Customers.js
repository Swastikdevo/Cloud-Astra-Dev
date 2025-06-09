```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [filter, setFilter] = useState('');
  
  useEffect(() => {
    fetch('https://api.example.com/customers')
      .then(res => res.json())
      .then(data => setCustomers(data));
  }, []);
  
  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };
  
  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input type="text" placeholder="Filter by name" value={filter} onChange={handleFilterChange} />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```