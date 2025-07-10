```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortOrder, setSortOrder] = useState('asc');

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
    setLoading(false);
  };

  const handleSort = () => {
    const sortedCustomers = [...customers].sort((a, b) => {
      if (sortOrder === 'asc') {
        return a.name.localeCompare(b.name);
      } else {
        return b.name.localeCompare(a.name);
      }
    });
    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    setCustomers(sortedCustomers);
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <button onClick={handleSort}>Sort by Name</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```