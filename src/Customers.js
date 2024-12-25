```javascript
import React, { useState, useEffect } from 'react';

const CustomerSearch = ({ customers }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredCustomers, setFilteredCustomers] = useState(customers);

  useEffect(() => {
    const result = customers.filter(customer =>
      customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredCustomers(result);
  }, [searchTerm, customers]);

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search Customers" 
        value={searchTerm} 
        onChange={e => setSearchTerm(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerSearch;
```