```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sort, setSort] = useState('asc');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        setLoading(false);
      });
  }, []);

  const handleSort = () => {
    const sortedCustomers = [...customers].sort((a, b) => {
      return sort === 'asc' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name);
    });
    setCustomers(sortedCustomers);
    setSort(sort === 'asc' ? 'desc' : 'asc');
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Customer List</h2>
      <button onClick={handleSort}>Sort by Name ({sort})</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```