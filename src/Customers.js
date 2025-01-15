```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setLoading(false);
    };
    fetchCustomers();
  }, []);

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management System</h1>
      <input
        type="text"
        placeholder="Search Customer"
        value={filter}
        onChange={handleFilterChange}
      />
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {filteredCustomers.map(customer => (
            <li key={customer.id}>
              {customer.name} - {customer.email}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomerManagement;
```