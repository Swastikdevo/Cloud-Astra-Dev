```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setLoading(false);
    };
    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1>Customer List</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <input
            type="text"
            placeholder="Search..."
            value={filter}
            onChange={e => setFilter(e.target.value)}
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

export default CustomerList;
```