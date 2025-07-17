```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = ({ customers }) => {
  const [filter, setFilter] = useState('');
  const [sortedCustomers, setSortedCustomers] = useState([]);

  useEffect(() => {
    const filtered = customers.filter(customer => 
      customer.name.toLowerCase().includes(filter.toLowerCase()));
    setSortedCustomers(filtered.sort((a, b) => a.name.localeCompare(b.name)));
  }, [filter, customers]);

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search Customers" 
        value={filter} 
        onChange={(e) => setFilter(e.target.value)} 
      />
      <ul>
        {sortedCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```