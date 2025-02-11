```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        setCustomers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, []);

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      {error && <p>Error: {error.message}</p>}
      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <input
            type="text"
            placeholder="Search customers"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <ul>
            {filteredCustomers.map(customer => (
              <li key={customer.id}>
                {customer.name} - {customer.email}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export default CustomerManagement;
```