```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('/api/customers');
        if (!response.ok) throw new Error('Failed to fetch customers');
        const data = await response.json();
        setCustomers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        placeholder="Filter by name" 
        value={filter}
        onChange={(e) => setFilter(e.target.value)} 
      />
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {filteredCustomers.length > 0 ? (
        <ul>
          {filteredCustomers.map(customer => (
            <li key={customer.id}>{customer.name}</li>
          ))}
        </ul>
      ) : (
        <p>No customers found</p>
      )}
    </div>
  );
};

export default CustomerManagement;
```