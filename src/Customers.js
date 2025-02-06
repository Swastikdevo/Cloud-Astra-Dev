```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        setLoading(false);
      });
  }, []);

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search customers..." 
        value={filter} 
        onChange={handleFilterChange} 
      />
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {filteredCustomers.map(customer => (
            <li key={customer.id}>{customer.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomerList;
```