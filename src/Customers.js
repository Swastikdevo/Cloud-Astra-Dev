```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);
  
  const handleFilterChange = (event) => {
    setFilter(event.target.value);
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  const handleDeleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <input
        type="text"
        placeholder="Search customers..."
        value={filter}
        onChange={handleFilterChange}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```