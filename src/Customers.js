```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('/api/customers');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        setCustomers(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management System</h1>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error.message}</p>}
      <input
        type="text"
        placeholder="Search customers"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```